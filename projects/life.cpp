#include <iostream>
using namespace std;
struct{
    int age;
    string name;
    double  height;
    float weight;
    string school_name; 
    string major;
} life;

int main(){
    life.age=20;
    life.name="ferdinard afful bentum";
    life.height=5.11;
    life.weight=150.5;
    life.school_name="university of Ghana,legon";
    life.major="computer science";
      
    cout << life.age << endl;
    cout << life.name << endl;
    cout << life.height << endl;
    cout << life.weight << endl;
    cout << life.school_name << endl;
    cout << life.major << endl;
    return 0;
}
