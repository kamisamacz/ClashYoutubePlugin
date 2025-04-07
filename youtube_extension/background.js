// Změna ikony a stavu
let isActive = false;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  switch (request.action) {
    case "updateIcon":
      isActive = request.active;
      updateToolbarIcon(isActive);
      break;
    case "getState":
      sendResponse({ active: isActive });
      break;
  }
});

function updateToolbarIcon(active) {
  const iconPath = active ? "icons/icon_active.png" : "icons/icon16.png";
  chrome.action.setIcon({ path: iconPath });
}

// Uložení stavu při restartu
chrome.runtime.onStartup.addListener(() => {
  chrome.storage.local.get(['overlayActive'], (result) => {
    if (result.overlayActive) {
      updateToolbarIcon(true);
    }
  });
});