function copy() {
     var text = document.getElementById("copy_text");
     text.select();
     document.execCommand("copy");
}
