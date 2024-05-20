document.addEventListener('DOMContentLoaded', (event) => {
    let questionNumber = 1;

    const makeCellEditable = (cell) => {
        cell.contentEditable = true;
        cell.classList.add('editable');
    };

    const makeCellNonEditable = (cell) => {
        cell.contentEditable = false;
        cell.classList.remove('editable');
    };

    const createTableFromCSV = (csvString) => {
        const rows = csvString.split('\n');
        const table = document.createElement('table');
        table.className = 'table table-striped';
        rows.forEach((row, rowIndex) => {
            const tr = document.createElement('tr');
            const cells = row.split(',');
            cells.forEach((cell, cellIndex) => {
                const cellElement = rowIndex === 0 ? document.createElement('th') : document.createElement('td');
                cellElement.innerHTML = formatCellContent(cell);
                if (rowIndex !== 0) {
                    cellElement.addEventListener('click', () => {
                        if (!cellElement.classList.contains('editable')) {
                            makeCellEditable(cellElement);
                            cellElement.focus();
                        }
                    });
                    cellElement.addEventListener('blur', () => {
                        if (cellElement.classList.contains('editable')) {
                            makeCellNonEditable(cellElement);
                        }
                    });
                }
                tr.appendChild(cellElement);
            });
            table.appendChild(tr);
        });
        return table;
    };

    const formatCellContent = (content) => {
        if (content.length > 100) {
            const truncated = content.slice(0, 100);
            return `
                <div class="expandable">
                    <span class="truncated">${truncated}...</span>
                    <span class="full-content">${content}</span>
                    <span class="expand-btn">Read more</span>
                </div>
            `;
        }
        return content;
    };

    const tableContainer = document.getElementById('table-container');
    fetch('data/students_submissions.csv')
        .then(response => response.text())
        .then(csvString => {
            const table = createTableFromCSV(csvString);
            tableContainer.appendChild(table);

            // Add event listeners for expand/collapse functionality
            document.querySelectorAll('.expandable .expand-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const expandable = btn.parentElement;
                    expandable.classList.toggle('expanded');
                    btn.textContent = expandable.classList.contains('expanded') ? 'Read less' : 'Read more';
                });
            });
        });

    document.getElementById('saveButton').addEventListener('click', () => {
        const table = document.querySelector('.table');
        const rows = table.querySelectorAll('tr');
        const csvData = [];
        rows.forEach((row, index) => {
            const cells = row.querySelectorAll('th, td');
            const rowData = Array.from(cells).map(cell => cell.textContent.trim());
            csvData.push(rowData.join(','));
        });

        const csvString = csvData.join('\n');
        const blob = new Blob([csvString], { type: 'text/csv' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'students_submissions.csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    document.getElementById('addQuestionButton').addEventListener('click', () => {
        const table = document.querySelector('.table');
        const rows = table.rows;

        const headerRow = rows[0];
        const newHeaderCell = headerRow.insertCell(-1);
        newHeaderCell.textContent = 'Question ' + questionNumber;

        for (let i = 1; i < rows.length; i++) {
            const newCell = rows[i].insertCell(-1);
            makeCellEditable(newCell);
        }

        questionNumber++;
    });
});

