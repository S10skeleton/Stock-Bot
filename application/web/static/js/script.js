document.addEventListener('DOMContentLoaded', () => {
    // 1) Get the list of symbols for the dropdown
    fetch('/api/symbols')
      .then(response => response.json())
      .then(symbols => {
        populateDropdown(symbols);
      })
      .catch(err => console.error('Error fetching symbols:', err));
  
    // 2) Attach event to the "Load Data" button
    const loadDataBtn = document.getElementById('loadDataBtn');
    loadDataBtn.addEventListener('click', () => {
      const dropdown = document.getElementById('symbolDropdown');
      const selectedSymbol = dropdown.value;
      fetchMarketData(selectedSymbol);
    });
  });
  
  function populateDropdown(symbols) {
    const dropdown = document.getElementById('symbolDropdown');
    dropdown.innerHTML = ''; // Clear any existing options
  
    symbols.forEach(symbol => {
      const option = document.createElement('option');
      option.value = symbol;
      option.text = symbol;
      dropdown.appendChild(option);
    });
  }
  
  function fetchMarketData(symbol) {
    // calls /api/market-data/SYMBOL
    fetch(`/api/market-data/${symbol}`)
      .then(response => response.json())
      .then(data => {
        renderMarketDataTable(data);
      })
      .catch(err => console.error('Error fetching market data:', err));
  }
  
  function renderMarketDataTable(data) {
    const tableBody = document.querySelector('#marketDataTable tbody');
    tableBody.innerHTML = ''; // Clear existing rows
  
    data.forEach(item => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${item.symbol}</td>
        <td>${item.date}</td>
        <td>${item.open.toFixed(2)}</td>
        <td>${item.high.toFixed(2)}</td>
        <td>${item.low.toFixed(2)}</td>
        <td>${item.close.toFixed(2)}</td>
        <td>${item.volume}</td>
      `;
      tableBody.appendChild(row);
    });
  }
  