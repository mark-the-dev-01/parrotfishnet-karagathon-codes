let deviceData = [];

fetch(
  "https://20200827t003648-dot-marine-protected-areas-v279620.et.r.appspot.com/dashboard/api/alldata"
)
  .then((res) => res.json())
  .then((data) => {
    // this.setState({ devices: data });
    deviceData = data;
    console.log(data);
  })
  .catch(console.log);

export default deviceData;
