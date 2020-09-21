#include <stdio.h>
#include <stdlib.h>
typedef struct student  student;
typedef struct student *studptr;
typedef struct course  course;
typedef struct course *couptr;
typedef struct registration  registration;
typedef struct registration * regptr;
regptr *head;

struct student{
  int id ;
  char name [30];
  double gpa ;
  int ch;
};
struct course{
  int id ;
  char name [30];
  char code[10] ;
  int ch;
};

struct registration {

  studptr student;
  couptr course;
  regptr next ;
};
student students [10]={{1,"ahmed",3.9,18},{2,"fawzi",2.9,18},
                         {3,"saed",3.8,18},{4,"abdlhamed",3.3,18},
                         {5,"said",3.7,18},{6,"abdalah",3.2,18},
                         {7,"manal",3.6,18},{8,"omar",3.1,18},
                         {9,"manar",3.5,18},{10,"abdelrahman",2.2,18}};
  course courses [3]={{1,"oop","a1",3},
                      {2,"problem solving","b5",3}
                    , {5,"adv programing","c11",3}};
void displayallstudent(){
    for(int i = 0;i< 10;i++)
    {
        printf("%d - %s - %lf - %d\n",students[i].id,students[i].name, students[i].gpa, students[i].ch);
    }
    printf("\n");
}

void displayallcourse(){

    for(int i = 0;i< 3;i++)
    {
        printf("%d - %s - %s - %d\n\n", courses[i].id, courses[i].code, courses[i].name, courses[i].ch);
    }
    printf("\n");

}

void register_course_to_student(int course_id, int student_id){

    bool found_course = false;
    bool found_student = false;

    struct course* chosen_course;
    struct student* chosen_student;

    for(int i = 0;i < 10;i++)
    {
        if(student_id == students[i].id)
        {
            printf("%s is Found\n", students[i].name);
            chosen_student = &students[i];
            found_student = true;
            break;
        }

    }
    if(found_student == false)
    {
        printf("This ID of course does not exist\n");
        return;
    }
    for(int i = 0;i < 3;i++)
    {
        if(course_id == courses[i].id)
        {
            printf("%s is Found\n", courses[i].name);
            chosen_course = &courses[i];
            found_course = true;
            break;
        }
    }
    if(found_course == false)
    {
       printf("This ID of course does not exist\n");
       return;
    }


    }









int main(void) {

while(true){
  printf("\n1- Display all students.\n2- Display all courses.\n3- Register course to student.\n4- Withdraw course from student.\n5- Display Student Schedule.\n6- Display Course Schedule.\n0- Exit the program.\n");
  int x;
  printf("\nchoose number \n");
  scanf("%d",&x);
 if (x == 1){
      displayallstudent();
  }
 if (x == 2){
    displayallcourse();
 }
 if (x == 3){
        int course_id = 0;
        int student_id = 0;

        printf("Enter Course ID: ");
        scanf("%d",&course_id);

        printf("Enter Student ID: ");
        scanf("%d",&student_id);

        register_course_to_student(course_id, student_id);

 }
}


return 0;
}
