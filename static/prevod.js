function prevod(){
  $.fn.bootstrapTable.locales['sl-SI'] = {
    formatLoadingMessage: function () {
      return 'Nalaganje, prosimo počakajte ...';
    },
    formatRecordsPerPage: function (pageNumber) {
      return pageNumber + ' vrstic na stran';
    },
    formatShowingRows: function (pageFrom, pageTo, totalRows) {
      return 'Prikazujem ' + pageFrom + ' do ' + pageTo + ' od skupaj ' + totalRows + ' vrstic';
    },
    formatSearch: function () {
      return 'Iskanje';
    },
    formatNoMatches: function () {
      return 'Ni najdenih rezultatov.';
    },
    formatPaginationSwitch: function () {
      return 'Prikaži/skrij številčenje strani';
    },
    formatRefresh: function () {
      return 'Osveži';
    },
    formatToggle: function () {
      return 'Preklopi';
    },
    formatColumns: function () {
      return 'Stolpci';
    },
    formatExport: function () {
      return 'Izvozi podatke';
    },
    formatClearFilters: function () {
      return 'Počisti filtre';
    },
  };

  $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['sl-SI']);
}
