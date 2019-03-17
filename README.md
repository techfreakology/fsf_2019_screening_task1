# fsf_2019_screening_task1
Fosse Summer Fellowship task 2

Task Description:

Create a Task Manager Django App using Django, that does the following:

  1.Authenticate the user
      1.Allow new users to sign up
      2.Allow existing users to sign in

  2.Allow only an authenticated user to create Task

  3.Allow creation of ‘Teams’
    1.Team creator should be able to add other Users to their Teams

  4.Only the Task Creator can edit Tasks that have been created by himself
    1.Other users from the same team can only view and comment on Tasks that were created by another User

  5.A User from another Team cannot view/edit/assign/comment on a Task of a different Team Member.
    1.Creator of Task should be able to assign the Task to one or more Users from his own Team

  6.In case Task Creator does not belong to a team, he himself will always be assigned to his own tasks.

  7.Tasks should have the Fields: Title, Description, Assignee and Status (Planned, Inprogress, Done etc.)

  8.Each Task should have a comments section where all users in one Team can comment on the Task

  9.An authenticated User can comment on his own tasks (assigned to or created by him) as well as other Tasks of his Team members.

  10.Write Test Cases for your Django App.