console.log("WEE");

const defaultTable =
  "<tr><th>Id</th><th>Next</th><th>MSG</th><th>Date</th></tr>";

const infoTable = document.getElementById("infotable");

const fillTable = async (count = 5, offset = 0, table = infoTable) => {
  const resp = await fetch(`/api/linkGets?count=${count}&offset=${offset}`);
  const list = await resp.json();
  table.innerHTML = defaultTable;
  console.log(list);
  for (const info of list) {
    const row = document.createElement("tr");
    const idTd = document.createElement("td");
    const msgTd = document.createElement("td");
    const nextTd = document.createElement("td");
    const dateTd = document.createElement("td");

    const idText = info["id"];
    const msgText = info["msg"];
    const linkText = info["link"];
    const dateText = new Date(info["date"]).toISOString();

    const idTextEle = document.createTextNode(idText);
    const msgTextEle = document.createTextNode(msgText);
    const nextTextEle = document.createTextNode(linkText);
    const dateTextEle = document.createTextNode(dateText);
    idTd.appendChild(idTextEle);
    msgTd.appendChild(msgTextEle);
    nextTd.appendChild(nextTextEle);
    dateTd.appendChild(dateTextEle);

    row.appendChild(idTd);
    row.appendChild(msgTd);
    row.appendChild(nextTd);
    row.appendChild(dateTd);

    table.appendChild(row);
  }
};
const main = async () => {
  const resp = await fetch(`/api/count`);
  const count = await resp.json();
  document.getElementById("offset").value = count;
  console.log(count);
  fillTable(5, count, infoTable);
};

window.onload = main();

const changePage = (posNeg) => {
  const count = parseInt(document.getElementById("count").value);
  const offset = parseInt(document.getElementById("offset").value);
  console.log(`${count} ${offset}`);
  if (count == NaN || offset == NaN) {
    return;
  }
  const move = Math.max(count * posNeg + offset, 0);
  document.getElementById("offset").value = move;
  fillTable(count, move, infoTable);
};

document.getElementById("prevBtn").onclick = (ee) => {
  changePage(1);
};
document.getElementById("nextBtn").onclick = (ee) => {
  changePage(-1);
};

document.getElementById("countForm").onchange = (ee) => {
  const count = parseInt(document.getElementById("count").value);
  const offset = parseInt(document.getElementById("offset").value);
  if (count == NaN || offset == NaN) {
    return;
  }
  console.log(count);
  fillTable(count, offset, infoTable);
};
