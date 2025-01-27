let tableData = [
  { id: '#0019215LMBS', admin: 'Benjamin Atakhora', email: 'nangrahills@gmail.com', school: 'Best Brain Academy', status: 'Active', date: 'Tue, Jan 24, 2023 04:40 PM' },
  { id: '#0019215LMBS', admin: 'Benjamin Akohora', email: 'nangrahills@gmail.com', school: 'Great Jesus Int. School', status: 'Deactivated', date: 'Tue, Jan 24, 2023 04:40 PM' },
  { id: '#0019215LMBS', admin: 'Benjamin Akohora', email: 'nangrahills@gmail.com', school: 'Best Brain Academy', status: 'Expired', date: 'Tue, Jun 13, 2023 10:40 PM' },
  { id: '#0019215LMBS', admin: 'Benjamin Akohora', email: 'nangrahills@gmail.com', school: 'Best Brain Academy', status: 'Deactivated', date: 'Tue, Jan 24, 2023 04:40 PM' },
  { id: '#0019215LMBS', admin: 'Benjamin Akohora', email: 'nangrahills@gmail.com', school: 'Best Brain Academy', status: 'Expired', date: 'Tue, Jun 13, 2023 10:40 PM' },
  { id: '#0019215LMBS', admin: 'Benjamin Akohora', email: 'nangrahills@gmail.com', school: 'Best Brain Academy', status: 'Active', date: 'Tue, Jan 24, 2023 04:40 PM' },
];

const rowsPerPage = 6;
let currentPage = 1;

function renderTable() {
  const tbody = document.querySelector('tbody');
  tbody.innerHTML = '';

  const start = (currentPage - 1) * rowsPerPage;
  const end = start + rowsPerPage;
  const currentRows = tableData.slice(start, end);

  currentRows.forEach(row => {
    const tr = document.createElement('tr');
    tr.classList.add(row.status.toLowerCase());
    tr.innerHTML = `
      <td>${row.id}</td>
      <td>${row.admin}</td>
      <td>${row.email}</td>
      <td>${row.school}</td>
      <td>
        <span class="status ${row.status.toLowerCase()}">
          ${getSVGIcon(row.status)} ${row.status}
        </span>
      </td>
      <td>${row.date}</td>
      <td>
        <div class="more-options-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" fill="none">
            <g filter="url(#filter0_d_249_14568)">
              <rect x="4" y="4" width="24" height="24" rx="12" fill="#F4F5F6"/>
              <path d="M12 16C12 16.8837 11.2837 17.6 10.4 17.6C9.51639 17.6 8.80005 16.8837 8.80005 16C8.80005 15.1164 9.51639 14.4 10.4 14.4C11.2837 14.4 12 15.1164 12 16Z" fill="#101828"/>
              <path d="M17.6 16C17.6 16.8837 16.8837 17.6 16 17.6C15.1164 17.6 14.4 16.8837 14.4 16C14.4 15.1164 15.1164 14.4 16 14.4C16.8837 14.4 17.6 15.1164 17.6 16Z" fill="#101828"/>
              <path d="M23.2 16C23.2 16.8837 22.4837 17.6 21.6 17.6C20.7164 17.6 20 16.8837 20 16C20 15.1164 20.7164 14.4 21.6 14.4C22.4837 14.4 23.2 15.1164 23.2 16Z" fill="#101828"/>
            </g>
            <defs>
              <filter id="filter0_d_249_14568" x="0" y="0" width="32" height="32" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                <feFlood flood-opacity="0" result="BackgroundImageFix"/>
                <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
                <feMorphology radius="4" operator="dilate" in="SourceAlpha" result="effect1_dropShadow_249_14568"/>
                <feOffset/>
                <feComposite in2="hardAlpha" operator="out"/>
                <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.2 0"/>
                <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_249_14568"/>
                <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_249_14568" result="shape"/>
              </filter>
            </defs>
          </svg>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function renderPagination() {
  const pagination = document.querySelector('.pagination');
  pagination.innerHTML = '';

  const totalPages = Math.ceil(tableData.length / rowsPerPage);
  for (let i = 1; i <= totalPages; i++) {
    const button = document.createElement('button');
    button.textContent = i;
    button.classList.add(i === currentPage ? 'active' : '');
    button.addEventListener('click', () => {
      currentPage = i;
      renderTable();
      renderPagination();
    });
    pagination.appendChild(button);
  }
}

function getSVGIcon(status) {
  switch (status.toLowerCase()) {
    case 'active':
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
      <path d="M12 6.00004C12 7.4728 10.8061 8.66671 9.33333 8.66671C7.86057 8.66671 6.66667 7.4728 6.66667 6.00004C6.66667 4.52728 7.86057 3.33337 9.33333 3.33337C10.8061 3.33337 12 4.52728 12 6.00004Z" fill="#00963E"/>
      <path d="M14.6667 13.6667C14.6667 15.3236 14.6667 16.6667 9.33333 16.6667C4 16.6667 4 15.3236 4 13.6667C4 12.0099 6.38781 10.6667 9.33333 10.6667C12.2789 10.6667 14.6667 12.0099 14.6667 13.6667Z" fill="#00963E"/>
      <path d="M16.3737 7.99889C16.5572 7.7925 16.5386 7.47646 16.3322 7.293C16.1258 7.10954 15.8098 7.12813 15.6263 7.33453L14.1828 8.95851L13.6678 8.49506C13.4626 8.31033 13.1464 8.32697 12.9617 8.53222C12.777 8.73748 12.7936 9.05362 12.9989 9.23835L13.8877 10.0384C13.9867 10.1274 14.1171 10.1733 14.25 10.1659C14.383 10.1585 14.5075 10.0984 14.5959 9.99889L16.3737 7.99889Z" fill="#00963E"/>
    </svg>`;
    case 'expired':
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
      <path d="M10.0001 8.66671C11.4728 8.66671 12.6667 7.4728 12.6667 6.00004C12.6667 4.52728 11.4728 3.33337 10.0001 3.33337C8.52732 3.33337 7.33341 4.52728 7.33341 6.00004C7.33341 7.4728 8.52732 8.66671 10.0001 8.66671Z" fill="#DE2525"/>
      <path fill-rule="evenodd" clip-rule="evenodd" d="M14.0001 12.5C12.8035 12.5 11.8334 13.4701 11.8334 14.6667C11.8334 15.8633 12.8035 16.8334 14.0001 16.8334C15.1967 16.8334 16.1667 15.8633 16.1667 14.6667C16.1667 13.4701 15.1967 12.5 14.0001 12.5ZM12.8334 14.6667C12.8334 14.0224 13.3557 13.5 14.0001 13.5C14.1376 13.5 14.2696 13.5238 14.3921 13.5675L12.9009 15.0588C12.8572 14.9362 12.8334 14.8042 12.8334 14.6667ZM13.608 15.7659L15.0992 14.2747C15.1429 14.3972 15.1667 14.5292 15.1667 14.6667C15.1667 15.311 14.6444 15.8334 14.0001 15.8334C13.8625 15.8334 13.7306 15.8096 13.608 15.7659Z" fill="#DE2525"/>
      <path d="M10.0001 16.6667C4.66675 16.6667 4.66675 15.3236 4.66675 13.6667C4.66675 12.0099 7.05456 10.6667 10.0001 10.6667C11.5797 10.6667 12.999 11.053 13.9755 11.6668C12.33 11.68 11.0001 13.018 11.0001 14.6667C11.0001 15.4077 11.2687 16.0859 11.7139 16.6093C11.2147 16.647 10.6466 16.6667 10.0001 16.6667Z" fill="#DE2525"/>
    </svg>`;
    case 'deactivated':
      return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
      <path d="M11.3333 6.00004C11.3333 7.4728 10.1393 8.66671 8.66658 8.66671C7.19383 8.66671 5.99992 7.4728 5.99992 6.00004C5.99992 4.52728 7.19383 3.33337 8.66658 3.33337C10.1393 3.33337 11.3333 4.52728 11.3333 6.00004Z" fill="#101828"/>
      <path d="M13.9999 13.6667C13.9999 15.3236 13.9999 16.6667 8.66658 16.6667C3.33325 16.6667 3.33325 15.3236 3.33325 13.6667C3.33325 12.0099 5.72107 10.6667 8.66658 10.6667C11.6121 10.6667 13.9999 12.0099 13.9999 13.6667Z" fill="#101828"/>
      <path d="M15.9631 8.07755C16.1583 7.88229 16.1583 7.56571 15.9631 7.37045C15.7678 7.17518 15.4512 7.17518 15.2559 7.37045L14.6667 7.95971L14.0774 7.37045C13.8822 7.17519 13.5656 7.17519 13.3703 7.37045C13.1751 7.56572 13.1751 7.8823 13.3703 8.07756L13.9596 8.66682L13.3703 9.25606C13.1751 9.45133 13.1751 9.76791 13.3703 9.96317C13.5656 10.1584 13.8822 10.1584 14.0774 9.96317L14.6667 9.37392L15.2559 9.96318C15.4512 10.1584 15.7678 10.1584 15.963 9.96318C16.1583 9.76792 16.1583 9.45133 15.963 9.25607L15.3738 8.66682L15.9631 8.07755Z" fill="#101828"/>
    </svg>`;
    default:
      return `<svg fill="black" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/></svg>`;
  }
}

renderTable();
renderPagination();