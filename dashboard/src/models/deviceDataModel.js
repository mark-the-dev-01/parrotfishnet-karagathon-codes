let deviceData = [];

fetch("http://localhost:5000/alldata")
  .then((res) => res.json())
  .then((data) => {
    // this.setState({ devices: data });
    deviceData = data;
    console.log(data);
  })
  .catch(console.log);

export default deviceData;
