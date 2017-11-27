
#define DOOR_HEIGHT 200 // in cm
#define MIN_PERSON_HEIGHT 150 // in cm
#define FLAG_PIN PD6 // pin to throw high when person walks through door
#define RESET_PIN PD7 // pin to reset flag


unsigned long distance[2] = {0,0};
int threshold = 20; //DOOR_HEIGHT - MIN_PERSON_HEIGHT;


void setup() {
  Serial.begin (9600);
  pinMode(PD3, OUTPUT);
  pinMode(PD5, OUTPUT);
  pinMode(PD2, INPUT);
  pinMode(PD4, INPUT);
  pinMode(PD6, OUTPUT);
}

int readHCSR04(int trigger, int echo){
    // send trigger
    digitalWrite(trigger, LOW);
    delayMicroseconds(2);
    digitalWrite(trigger, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigger, LOW);
    // wait for echo
    return (pulseIn(echo, HIGH)/58.2);
}

void readRangers(int trigPins[], int echoPins[], unsigned long times[], int num) {
  for (int i = 0; i < num; ++i) {
    times[i] = readHCSR04(trigPins[i],echoPins[i]);
  }
}

void loop() {
  int echoPins[2] = {PD2,PD4};
  int trigPins[2] = {PD3,PD5};

  readRangers(trigPins, echoPins, distance, 2);

  if (distance[0]<threshold || distance[1]<threshold) {
    digitalWrite(PD6, HIGH);
  } else {
    digitalWrite(PD6, LOW);
  }
  Serial.print(distance[0]);
  Serial.print(" cm; ");
  Serial.print(distance[1]);
  Serial.println(" cm");

  // TODO: determine optimal delay
  //delay(50);
}
