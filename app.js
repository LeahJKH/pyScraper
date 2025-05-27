async function fetchJobs(query, locations) {
  try {
    const response = await fetch('http://localhost:5000/api/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, locations }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    console.log(data.jobs)
    data.jobs.forEach(e => {
      const div = document.createElement("div");
      const h2 = document.createElement("h2")
      const h2Txt = document.createTextNode(`${e.company_info[0]}, ${e.company_info[1]}`)

      const a = document.createElement("a")
      a.href = e.link
      const atxt = document.createTextNode(`link til annonse`);

      const p = document.createElement("p")
      const ptxt = document.createTextNode(`${e.title}`)
      p.append(ptxt)
      a.append(atxt)
      h2.append(h2Txt)

      div.appendChild(h2)
      div.appendChild(a)
      div.appendChild(p)
      const jobsSect = document.querySelector("#jobs")
      jobsSect.appendChild(div)
    });
  } catch (error) {
    console.error("Failed to fetch jobs:", error);
  }
}

const finn = document.querySelector("#click-for-finn")
const form = document.querySelector("#field-forms")

finn.addEventListener("click", (e) => {
  const div = document.createElement("div");

  const inputlocation = document.createElement("input");
  inputlocation.type = "text";
  inputlocation.placeholder = "Enter location";

  const inputquery = document.createElement("input");
  inputquery.type = "text";
  inputquery.placeholder = "What are you looking for?";

  const searchBtn = document.createElement("button");
  searchBtn.textContent = "Search";

  div.appendChild(inputlocation);
  div.appendChild(inputquery);
  div.appendChild(searchBtn);
  form.appendChild(div);

  searchBtn.addEventListener("click", () => {
    const locationValue = inputlocation.value.trim();
    const queryValue = inputquery.value.trim();

    if (locationValue && queryValue) {
      fetchJobs(queryValue, [locationValue]);
    } else {
      alert("Please fill in both fields before searching.");
    }
  });
});



