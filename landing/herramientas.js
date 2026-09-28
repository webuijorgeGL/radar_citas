(function () {
  "use strict";

  var STORAGE_KEY = "radar-document-checklist-v1";
  var checklist = document.getElementById("document-checklist");
  var count = document.getElementById("checklist-count");
  var progress = document.getElementById("checklist-progress");

  function emit(eventName, parameters) {
    if (typeof window.gtag === "function") window.gtag("event", eventName, parameters || {});
  }

  function checkedKeys() {
    return Array.from(checklist.querySelectorAll("input:checked")).map(function (input) { return input.dataset.check; });
  }

  function renderProgress() {
    var current = checkedKeys().length;
    var total = checklist.querySelectorAll("input").length;
    count.textContent = current + " de " + total + " documentos marcados";
    progress.max = total;
    progress.value = current;
  }

  try {
    var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    checklist.querySelectorAll("input").forEach(function (input) { input.checked = saved.indexOf(input.dataset.check) !== -1; });
  } catch (error) {
    localStorage.removeItem(STORAGE_KEY);
  }
  renderProgress();

  checklist.addEventListener("change", function () {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(checkedKeys()));
    renderProgress();
    emit("checklist_update", { checked_count: checkedKeys().length });
  });

  document.getElementById("reset-checklist").addEventListener("click", function () {
    checklist.querySelectorAll("input").forEach(function (input) { input.checked = false; });
    localStorage.removeItem(STORAGE_KEY);
    renderProgress();
    emit("checklist_reset");
  });

  var subjectForm = document.getElementById("subject-form");
  var subjectResult = document.getElementById("subject-result");
  var subjectOutput = document.getElementById("subject-output");
  subjectForm.addEventListener("submit", function (event) {
    event.preventDefault();
    var name = document.getElementById("subject-name").value.trim().replace(/\s+/g, " ");
    var nit = document.getElementById("subject-nit").value.replace(/[^0-9-]/g, "");
    var date = document.getElementById("subject-date").value.replace(/-/g, "");
    if (!name || !nit || !date) return;
    subjectOutput.textContent = "Solicitud Devolucion Vehiculos eléctricos o híbridos - " + name + " - " + nit + " - " + date;
    subjectResult.hidden = false;
    document.getElementById("copy-status").textContent = "";
    emit("email_subject_generated");
  });

  document.getElementById("copy-subject").addEventListener("click", function () {
    var value = subjectOutput.textContent;
    if (!value) return;
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
      document.getElementById("copy-status").textContent = "Selecciona y copia el texto manualmente.";
      return;
    }
    navigator.clipboard.writeText(value).then(function () {
      document.getElementById("copy-status").textContent = "Copiado";
      emit("email_subject_copied");
    }).catch(function () {
      document.getElementById("copy-status").textContent = "Selecciona y copia el texto manualmente.";
    });
  });

  var offices = [
    ["Armenia", "dsia_armenia_devoluciones@dian.gov.co"], ["Arauca", "dsia_arauca_devoluciones@dian.gov.co"],
    ["Barrancabermeja", "dsia_barrancabermeja_devoluciones@dian.gov.co"], ["Barranquilla", "dsi_barranquilla_devoluciones@dian.gov.co"],
    ["Bogotá — persona natural", "dsi_bogota_recaudo_naturales@dian.gov.co"], ["Bogotá — persona jurídica", "dsi_bogota_recaudo_juridicas@dian.gov.co"],
    ["Bucaramanga", "dsia_bucaramanga_devoluciones@dian.gov.co"], ["Buenaventura", "dsia_buenaventura_devoluciones@dian.gov.co"],
    ["Cali", "dsi_cali_devoluciones@dian.gov.co"], ["Cartagena", "dsi_cartagena_devoluciones@dian.gov.co"],
    ["Cúcuta", "dsi_cucuta_devoluciones@dian.gov.co"], ["Florencia", "dsia_florencia_devoluciones@dian.gov.co"],
    ["Girardot", "dsia_girardot_devoluciones@dian.gov.co"], ["Grandes Contribuyentes", "dsi_grandesc_devoluciones@dian.gov.co"],
    ["Ibagué", "dsia_ibague_devoluciones@dian.gov.co"], ["Leticia", "dsia_leticia_devoluciones@dian.gov.co"],
    ["Manizales", "dsia_manizales_devoluciones@dian.gov.co"], ["Medellín", "dsi_medellin_devoluciones@dian.gov.co"],
    ["Montería", "dsia_monteria_devoluciones@dian.gov.co"], ["Neiva", "dsia_neiva_devoluciones@dian.gov.co"],
    ["Palmira", "dsia_palmira_devoluciones@dian.gov.co"], ["Pasto", "dsia_pasto_devoluciones@dian.gov.co"],
    ["Pereira", "dsia_pereira_devoluciones@dian.gov.co"], ["Popayán", "dsia_popayan_devoluciones@dian.gov.co"],
    ["Quibdó", "dsia_quibdo_devoluciones@dian.gov.co"], ["Riohacha", "dsia_riohacha_devoluciones@dian.gov.co"],
    ["San Andrés", "dsia_sanandres_devoluciones@dian.gov.co"], ["Santa Marta", "dsia_stamarta_devoluciones@dian.gov.co"],
    ["Sincelejo", "dsia_sincelejo_devoluciones@dian.gov.co"], ["Sogamoso", "dsia_sogamoso_devoluciones@dian.gov.co"],
    ["Tuluá", "dsia_tulua_devoluciones@dian.gov.co"], ["Tunja", "dsia_tunja_devoluciones@dian.gov.co"],
    ["Valledupar", "dsia_valledupar_devoluciones@dian.gov.co"], ["Villavicencio", "dsia_villavicencio_devoluciones@dian.gov.co"],
    ["Yopal", "dsia_yopal_devoluciones@dian.gov.co"]
  ];
  var select = document.getElementById("office-select");
  offices.forEach(function (office) {
    var option = document.createElement("option"); option.value = office[1]; option.textContent = office[0]; select.appendChild(option);
  });
  select.addEventListener("change", function () {
    var result = document.getElementById("mailbox-result");
    if (!select.value) { result.hidden = true; return; }
    var link = document.getElementById("mailbox-link");
    link.href = "mailto:" + select.value; link.textContent = select.value;
    document.getElementById("mailbox-note").textContent = "Verifica esta dirección en las instrucciones vigentes antes de enviar documentos.";
    result.hidden = false;
    emit("sectional_mailbox_viewed");
  });
})();
