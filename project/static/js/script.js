
myButton.addEventListener("click", function () {
  myPopup.classList.add("show");
});
closePopup.addEventListener("click", function () {
  myPopup.classList.remove("show");
});
window.addEventListener("click", function (event) {
  if (event.target == myPopup) {
    myPopup.classList.remove("show");
  }
});

function deleteTrip(id) {
  var v = new XMLHttpRequest();
  v.open("POST", "/deleteTrip", true);
  v.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  v.send("id=" + id);
  v.onload = function () {
    if (v.status === 200) {
      alert("Trip deleted");
      window.location.reload();
    }
  };
}
// function add() {
//   var v = document.getElementById("addForm");

//   if (v.style.display === "" || v.style.display === "none") {
//     document.getElementById("addForm").style.display = "block";
//   } else {
//     document.getElementById("addForm").style.display = "none";
//   }
// }

function deleteItem(id) {
  var v = new XMLHttpRequest();
  v.open("POST", "/deleteItem", true);
  v.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  v.send("id=" + id);
  v.onload = function () {
    if (v.status === 200) {
      alert("Item deleted");
      window.location.reload();
    }
  };
}
function deleteall(id) {
  var v = new XMLHttpRequest();
  v.open("POST", "/deleteItemAll", true);
  v.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  v.send("tripId=" + id);
  v.onload = function () {
    if (v.status === 200) {
      alert("All Items deleted");
      window.location.reload();
    }
  };
}
