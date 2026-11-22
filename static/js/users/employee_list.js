document.addEventListener("DOMContentLoaded", function () {
  // 1. Initial Page Load Setup
  const rows = document.querySelectorAll("tbody tr");

  rows.forEach((row) => {
    const isAdminCb = row.querySelector(
      'input[type="checkbox"][name$="is_admin"]',
    );
    if (!isAdminCb) return;

    const otherCbs = row.querySelectorAll(
      'input[type="checkbox"]:not([name$="is_admin"])',
    );

    if (isAdminCb.checked) {
      if (!request_user_is_owner) {
        // Non-owner viewing an admin
        isAdminCb.disabled = true;
      }
      otherCbs.forEach((cb) => (cb.disabled = true));
    } else {
      // If the employee is not an admin, non-owners shouldn't be able to grant admin status
      if (!request_user_is_owner) {
        isAdminCb.disabled = true;
      }
    }
  });
});

document.addEventListener("change", function (event) {
  const target = event.target;

  // Target 'is_admin' checkboxes (accounting for Django formset naming like 'form-0-is_admin')
  if (
    target &&
    target.type === "checkbox" &&
    target.name &&
    target.name.endsWith("is_admin")
  ) {
    const row = target.closest("tr");
    if (!row) return;

    const checkboxes = row.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach((cb) => {
      if (cb === target) return; // Skip the is_admin checkbox itself

      if (target.checked) {
        // Save the current state before overriding, if not already saved
        if (cb.dataset.prevState === undefined) {
          cb.dataset.prevState = cb.checked ? "true" : "false";
        }
        cb.checked = true;
        cb.disabled = true;
      } else {
        // Revert to the pre-check state and re-enable
        if (cb.dataset.prevState !== undefined) {
          cb.checked = cb.dataset.prevState === "true";
          delete cb.dataset.prevState;
        }
        cb.disabled = false;
      }
    });
  }
});
