document.addEventListener('DOMContentLoaded', () => {
    fetchMarketData();
  });
  
  function fetchMarketData() {
    // Calls the Flask API endpoint
    fetch('/api/market-data')
      .then(response => response.json())
      .then(data => {
        // data is an array of objects
        // e.g., [{ symbol: 'AAPL', date: '2025-01-08 09:31:00', open: 150.25, ... }, ...]
        renderMarketDataTable(data);
      })
      .catch(error => console.error('Error fetching market data:', error));
  }
  
  function renderMarketDataTable(data) {
    const tableBody = document.querySelector('#marketDataTable tbody');
    // Clear existing rows
    tableBody.innerHTML = '';
  
    // Create a row for each entry
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
  