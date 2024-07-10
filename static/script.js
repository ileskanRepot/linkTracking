console.log("WEE");

const fillTable = async (count, offset, table) => {
  const resp = await fetch(`/api/linkGets?count=${count}&offset=${offset}`);
  const list = await resp.json();
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
const infoTable = document.getElementById("infotable");
fillTable(2, 1, infoTable);
