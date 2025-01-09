document.addEventListener('DOMContentLoaded', () => {
  // 1) Fetch all symbols to populate the dropdown
  fetch('/api/symbols')
    .then(response => response.json())
    .then(symbols => {
      populateDropdown(symbols);
    })
    .catch(err => console.error('Error fetching symbols:', err));

  // 2) Set up the "Load Data" button click
  const loadDataBtn = document.getElementById('loadDataBtn');
  loadDataBtn.addEventListener('click', () => {
    const dropdown = document.getElementById('symbolDropdown');
    const symbol = dropdown.value;
    fetchMarketData(symbol);
  });
});

/**
 * Populate the symbolDropdown <select> with the given symbols array.
 */
function populateDropdown(symbols) {
  const dropdown = document.getElementById('symbolDropdown');
  dropdown.innerHTML = ''; // clear existing options

  symbols.forEach(sym => {
    const option = document.createElement('option');
    option.value = sym;
    option.text = sym;
    dropdown.appendChild(option);
  });
}

/**
 * Fetch market-data (including indicators) for the chosen symbol
 * and render it in the table.
 */
function fetchMarketData(symbol) {
  fetch(`/api/market-data/${symbol}`)
    .then(response => response.json())
    .then(data => {
      renderMarketDataTable(data);
    })
    .catch(err => console.error('Error fetching market data:', err));
}

/**
 * Render the data rows (with indicators) into the marketDataTable
 */
function renderMarketDataTable(data) {
  const tableBody = document.querySelector('#marketDataTable tbody');
  tableBody.innerHTML = ''; // clear existing rows

  data.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.date}</td>
      <td>${formatNum(item.open)}</td>
      <td>${formatNum(item.high)}</td>
      <td>${formatNum(item.low)}</td>
      <td>${formatNum(item.close)}</td>
      <td>${item.volume ?? ''}</td>
      
      <td>${formatNum(item.ma_50)}</td>
      <td>${formatNum(item.ma_200)}</td>
      <td>${formatNum(item.rsi_14)}</td>
      <td>${formatNum(item.macd)}</td>
      <td>${formatNum(item.macd_signal)}</td>
      <td>${formatNum(item.bb_upper)}</td>
      <td>${formatNum(item.bb_mid)}</td>
      <td>${formatNum(item.bb_lower)}</td>
    `;
    tableBody.appendChild(row);
  });
}

/**
 * Utility to format numeric values or return empty string if null/undefined
 */
function formatNum(value) {
  return (value !== null && value !== undefined) ? value.toFixed(2) : '';
}
