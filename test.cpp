/* C++ Programming Examples */
#include<iostream.h>
#include<conio.h>
void main()
{
	clrscr();
	int num;
	cout<<"Guess a Number : ";
	cin>>num;
	if(num>10 && num<100)
	{
		cout<<"What a mind!!";
	}
	else
	{
		cout<<"Opps..!!";
	}
	getch();
}