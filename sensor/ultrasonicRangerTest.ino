#define trigPin 5
#define echoPin 6
#define gnd 7
#define vcc 4

void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(gnd, OUTPUT);
  pinMode(vcc, OUTPUT);
  digitalWrite(vcc, HIGH);
  digitalWrite(gnd, LOW);
}

void loop() {
  long duration, distance;
  digitalWrite(trigPin, LOW);  // Added this line
  delayMicroseconds(2); // Added this line
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10); // Added this line
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  
  Serial.print(distance);
  Serial.println(" cm");
  
  delay(500);
}
