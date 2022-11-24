#include <Servo.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Int64.h>

// Definir COnstantes

int angleMax = 180; //maximum angle of the servos
int angleMin = 0; //minimum angle of the servos

// Variables
int angleToPass = 0;



char hello[13] = "Alive!";
char recieved[13] = "recieved!";
char focus[13] = "Focus!";
char wrong[13] = "Wrong!";

Servo zoomServo;
Servo focusServo;


ros::NodeHandle  nh;

std_msgs::String str_msg;

ros::Publisher chatter("chatter", &str_msg);

void messageCb( const std_msgs::Int64& toggle_msg){
  digitalWrite(7,HIGH);
  angleToPass = map(toggle_msg.data,0,100,0,180);
  recieved[11] = angleToPass+'0';
  str_msg.data = recieved;
  chatter.publish( &str_msg );
  zoomServo.write(angleToPass);

}

ros::Subscriber<std_msgs::Int64> sub1("zoomS", messageCb );

void focusCb( const std_msgs::Int64& focus_msg){
  digitalWrite(7,HIGH);
  angleToPass = map(focus_msg.data,0,100,0,180);
  recieved[11] = angleToPass+'0';
  str_msg.data = recieved;
  chatter.publish( &str_msg );
  focusServo.write(angleToPass);

}

ros::Subscriber<std_msgs::Int64> sub2("focusS", focusCb );



void setup()
{
  pinMode(7, OUTPUT);
  nh.initNode();
  nh.advertise(chatter);
  nh.subscribe(sub1);
  nh.subscribe(sub2);
  zoomServo.attach(9);
  focusServo.attach(10);
  zoomServo.write(180);
  focusServo.write(180);
}

void loop()
{
  str_msg.data = hello;
  chatter.publish( &str_msg );

  nh.spinOnce();
  
  delay(1000);

}
