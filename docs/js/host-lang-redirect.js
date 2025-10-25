(function () {
  try {
    var host = (window.location && window.location.hostname) || "";
    var path = (window.location && window.location.pathname) || "/";
    // если домен .ru и мы не на /ru/ — уводим на русскую локаль, сохраняя остальную часть пути
    if (host.endsWith(".ru") && !path.startsWith("/ru/")) {
      var newPath = "/ru" + (path === "/" ? "/" : path);
      var search = window.location.search || "";
      var hash = window.location.hash || "";
      window.location.replace(newPath + search + hash);
    }
  } catch (e) {}
})();
