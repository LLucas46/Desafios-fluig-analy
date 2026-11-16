/*
 * Complemento do formulário Fluig.
 * Configurar ds_laboratorios e os IDs das atividades após criar o processo no ambiente.
 * A validação final obrigatória pertence aos eventos de formulário/processo da Atividade 3.
 */
(function ($) {
  'use strict';

  var tableName = 'equipamentos';
  var stageByState = window.FLUIG_STAGE_BY_STATE || { '0': 'abertura' };

  function digits(value) { return String(value || '').replace(/\D/g, '').slice(0, 5); }
  function maskPatrimonio(input) {
    var value = digits(input.value);
    input.value = value ? 'SLG-' + value : '';
  }

  function applyMask(root) {
    (root || document).querySelectorAll('.js-patrimonio').forEach(function (input) {
      input.addEventListener('input', function () { maskPatrimonio(input); });
      input.addEventListener('blur', function () { maskPatrimonio(input); });
      if (input.value) maskPatrimonio(input);
    });
  }

  function setStage() {
    var state = String(window.WKNumState || '0');
    var active = stageByState[state] || 'abertura';
    document.querySelectorAll('.etapa-form').forEach(function (section) {
      var sectionStage = section.getAttribute('data-stage');
      section.classList.toggle('is-hidden', sectionStage !== active && sectionStage !== 'abertura');
      section.querySelectorAll('input, select, textarea, button').forEach(function (field) {
        if (sectionStage !== active) {
          if (field.type !== 'hidden') field.setAttribute('readonly', 'readonly');
          if (field.tagName === 'SELECT' || field.type === 'file' || field.type === 'radio' || field.type === 'checkbox' || field.tagName === 'BUTTON') field.disabled = true;
        }
      });
    });
  }

  function selectLaboratorio(value) {
    // Chame esta função no evento de retorno do zoom definido no Fluig Style Guide.
    var visible = document.getElementById('laboratorio');
    var code = document.getElementById('codigoLaboratorio');
    if (!value) return;
    visible.value = value.nome || value.NOME || '';
    code.value = value.codigo || value.CODIGO || '';
    visible.dispatchEvent(new Event('change', { bubbles: true }));
  }
  window.selecionarLaboratorio = selectLaboratorio;
  window.setSelectedZoomItem = function (item) {
    if (item && item.inputId === 'laboratorio') selectLaboratorio(item);
  };
  window.removedZoomItem = function (item) {
    if (item && item.inputId === 'laboratorio') {
      document.getElementById('codigoLaboratorio').value = '';
    }
  };

  function addRow() {
    if (window.wdkAddChild) {
      window.wdkAddChild(tableName);
      applyMask(document.getElementById(tableName));
      return;
    }
    var body = document.querySelector('#equipamentos tbody');
    var first = body && body.querySelector('tr');
    if (first) {
      var clone = first.cloneNode(true);
      clone.querySelectorAll('input').forEach(function (el) { el.value = ''; });
      clone.querySelectorAll('select').forEach(function (el) { el.selectedIndex = 0; });
      body.appendChild(clone);
      applyMask(clone);
    }
  }

  function removeRow(button) {
    var row = button.closest('tr');
    if (!row) return;
    if (window.wdkRemoveChild) { window.wdkRemoveChild(button); return; }
    var body = row.parentElement;
    if (body.querySelectorAll('tr').length > 1) row.remove();
  }

  document.addEventListener('click', function (event) {
    if (event.target.closest('[data-add-row]')) addRow();
    var remove = event.target.closest('[data-remove-row]');
    if (remove) removeRow(remove);
  });

  $(function () {
    applyMask(document);
    setStage();
  });
})(jQuery);
