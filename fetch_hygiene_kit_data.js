


fetch("https://opensheet.elk.sh/1omcx2qzhJ-Xv3Opvr-8rMg3nK5IRm85CfSnjg1qQze0/General Inventory")
  .then(res => res.json())
  .then(data => {

    console.log("Example row: ", data[20]);

    function extractAndSortSection(start, end) {
      return data
      .slice(start, end + 1)
      .filter(row => row["Item"] && row["Qty"])
      .map(row => ({
        Item: row["Item"].trim(),
        Qty: parseInt(row["Qty"]),
        }))
      .sort((a, b) => b.Qty - a.Qty);
      }

    const sections = {
      main: extractAndSortSection(19, 47),           // Rows 21–48
      first_aid_kit: extractAndSortSection(48, 54),  // Rows 50–55
      period_pack: extractAndSortSection(55, 60),    // Rows 57–61
      misc: extractAndSortSection(61, 67),           // Rows 63–68
      };

    console.log("Sorted sections:", sections);

    const outputDiv = document.getElementById("inventory-output");

      function renderSection(title, items) {
        const section = document.createElement("div");
        section.innerHTML = `
          <h3>${title}</h3>
          <ul>
            ${items
              .map(
                item => `<li>
                  ${item.Qty > 50 ? `<strong>${item.Item}</strong>` : item.Item}
                  – ${item.Qty}
                </li>`
              )
              .join("")}
          </ul>
        `;
        outputDiv.appendChild(section);
      }

      // Render all four sections
      renderSection("Main Hygiene Items", sections.main);
      renderSection("First Aid Kit", sections.first_aid_kit);
      renderSection("Period Pack", sections.period_pack);
      renderSection("Miscellaneous", sections.misc);

        })
  .catch(err => {
    console.error("Error loading sheet data:", err);
  });

