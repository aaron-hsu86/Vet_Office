#Vet_Office

Python project completed within a week.
Project uses MySQL to store and track data for Owners, their Pets, Doctors/Staff, Rooms at the office, and Appointments with pets conditions and treatment.

This is an MVP version of the project, and there are plenty of areas for improvement or to add more features.
At the moment, Rooms can be created, not deleted.
Client Info page is a massive list of Owners and Pet, not properly organized. It lists ALL information, not properly sorted and displayed.
All Appointments are listed.

TO-DO (if re-visiting this project in the future):
Appointments:
- Give Staff ability to create appointments from Staff page. - high priority
- Put completed appointments in a separate section. - normal priority
- Look into having the Staff page able to Live update the User side when the User arrives. - low priority
Rooms:
- Add a Edit Room feature to update room name or to delete a room. - normal priority
- Fix issue with Empty Room display. - low priority
- - Clarification: A room that has completed an appointment will display differently from a newly created / empty room. Has to do with returning a null/empty value from the SQL database and the checks determining what to display.
Clients:
- Organize Client Info page on Staff side to better display Clients and their pets. - normal priority
- - Maybe separate page for all Pets?
- - Links to owners with list of pets inside?
- - Or display all Owners and their Pets in sub-table
- Give Staff ability to edit Client information. - normal priority

CSS:
- Add more CSS to the project to make it more visually appealing. - low priority
- - Project was designed with a basic framework in mind and focus was on making it work. Not much effort was put into making it look nice.