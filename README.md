# recent_acquisitions
Python script to query Alma API for recent title data. Uses bibliographic record ids to query ILS, pull MARCXML, parse for local field data. This data is unavailable by default in ExLibris-provided Oracle instance.

*Instructions*
* Requires ```csv``` of MMS IDs in order to query Alma API.
  * Generate MMS IDs via Alma's Oracle Analytics instance.
  * Place ```csv```containing ```MMS Id``` column in root folder.
  * Run script
* Outputs ```txt```file to root folder

---

*To-Do*
* [ ] Add reqs file
* [ ] XPath explanation