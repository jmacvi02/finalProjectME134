**1. Problem**
There are numerous considerations when choosing a control method for a robot. Time for implementtion, behavior and design specifications, and personal preference/knowledge all play a part in this process. Balancing all of these factors can be difficult, and is a problem which roboticst regularly face. 

With this problem in mind, the purpose of this project was to make a meaningful comparision between a variety of different control methods: remote control of the XRP, classical autonomous control of the XRP, and ML control of the XRP. In comparing these control methods, we sought to better understand the benefits and downsides of each method so we could be more informed when selecting controllers in the future. 

**2. Approach**
To make a comparision between these methods, we first chose a task for the XRP to complete. We thought a challenging task with a clear definition of sucess was optimal for this project since a task of this nature makes it easier to compare between the control methods. We decided to have each XRP race around a rectangular track. Each XRP will have to complete 5 laps around the track. The average lap time and lap time varaition were chosen as meterics to compare between the methods. Additionally, we intended to reflect on the implementaiton processes of each as an extra qualitative comparision. 

To acheive remote control, we used an xbox controller, bluetooth, and a laptop. The xbox controller is connected to the computer via bluethooth which is then connected to the XRP via bluetooth as well. We first mapped the x and y postion of the xbox controller to a magnitude and angle. Then we mapped this magnitude and angle to motor efforts which we sent to the XRP. ELI TALK ABOUT MQTT STRUGGLES AND BLUETOOTH STUFF.

To acheive classic autonomous control, we implemented an offset line following algorithm. We used a trained Husky Lens Camera to detect a line along the top of the inner wall of the track. We calculated the slope and average y axis position of the line, and used these calculations to implement an PD controller with a target slope of 0 and y position of 80 (out of 240). To account for the XRP losing the inner wall, we implemented a simple state machine with main states of following and searching. The following state corresponds to the PD controller outlined above. The searching state commands the XRP to turn left until the inner wall in found. 

To acheive Ml control...
**3. Results**

**4. Impact**
