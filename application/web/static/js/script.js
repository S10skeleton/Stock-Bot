// script.js
// Handles fetching data from Flask endpoints and updating the DOM.

document.addEventListener('DOMContentLoaded', () => {
    fetchPortfolio();
    fetchPerformance();
  });
  
  function fetchPortfolio() {
    fetch('/api/portfolio')
      .then(response => response.json())
      .then(data => {
        const tableBody = document.querySelector('#portfolioTable tbody');
        tableBody.innerHTML = ''; // Clear existing rows if any
        data.forEach(item => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${item.symbol}</td>
            <td>${item.shares}</td>
            <td>${item.avg_price}</td>
          `;
          tableBody.appendChild(row);
        });
      })
      .catch(err => console.error('Error fetching portfolio:', err));
  }
  
  function fetchPerformance() {
    fetch('/api/performance')
      .then(response => response.json())
      .then(data => {
        const perfDiv = document.getElementById('performance');
        perfDiv.innerHTML = `
          <p>Total Value: $${data.totalValue}</p>
          <p>Unrealized PnL: $${data.unrealizedPnL}</p>
        `;
      })
      .catch(err => console.error('Error fetching performance:', err));
  }
  