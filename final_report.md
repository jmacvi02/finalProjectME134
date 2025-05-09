**1. Problem**
There are numerous considerations when choosing a control method for a robot. Time for implementtion, behavior and design specifications, and personal preference/knowledge all play a part in this process. Balancing all of these factors can be difficult, and is a problem which roboticst regularly face. 

With this problem in mind, the purpose of this project was to make a meaningful comparision between a variety of different control methods: remote control of the XRP, classical autonomous control of the XRP, and ML control of the XRP. In comparing these control methods, we sought to better understand the benefits and downsides of each method so we could be more informed when selecting controllers in the future. 

**2. Approach**
To make a comparision between these methods, we first chose a task for the XRP to complete. We thought a challenging task with a clear definition of sucess was optimal for this project since a task of this nature makes it easier to compare between the control methods. We decided to have each XRP race around a rectangular track. Each XRP will have to complete 5 laps around the track. The average lap time and lap time varaition were chosen as meterics to compare between the methods. Additionally, we intended to reflect on the implementaiton processes of each as an extra qualitative comparision. 

To achieve remote control, we used an Xbox controller and a laptop. At first, we established a BLE connection between the Xbox controller and the laptop, which was simultaneously running an MQTT server that broadcasted motor commands. The XRP was subscribed to the MQTT channel and listened for these commands. However, this workflow was more complicated than necessary, and it led to moderate to significant latency, oftentimes exceeding 3 seconds. We optimized the final workflow and cut our latency down. The Xbox controller and the XRP are connected to the laptop via BLE, with the laptop acting as the central hub for smoother command passage. We first mapped the x and y positions of the Xbox controller to a magnitude and angle. Then we mapped this magnitude and angle to motor efforts, which we sent to the XRP. 

To achieve classic autonomous control, we implemented an offset line following algorithm. We used a trained Husky Lens Camera to detect a line along the top of the inner wall of the track. We calculated the slope and average y axis position of the line, and used these calculations to implement an PD controller with a target slope of 0 and y position of 80 (out of 240). To account for the XRP losing the inner wall, we implemented a simple state machine with main states of following and searching. The following state corresponds to the PD controller outlined above. The searching state commands the XRP to turn left until the inner wall is found. 

To achieve ML control, we began by looking at larger libraries, such as Scikit or PyTorch. We figured that, like any other Python library, there would be a learning curve, but we were confident that we could put together a good ML script. Since these larger ML libraries cannot run on a lightweight microcontroller like the Pico, we initially planned to create a .pkl file and use an MQTT server to read motor measurements from the laptop to the XRP. However, upon further analysis, we realized that this was likely to be inefficient, since with MQTT comes latency. Therefore, we opted to extract the normalization data and program the math directly onto the Pico. This ensured that we would get the full benefits of the ML model while eliminating any sort of delay in the flow of data. 

**3. Results**

**4. Impact**
We have numerous takeways from completeing this project.

1. Remote control outperforms classic control for one time tasks: 
Using remote control, the XRP can complete laps significantly faster than the classic controller. This is because the classic control method we used does not adapt its base velocity depending on position on the track, whereas a human can do this manually via remote control. Thus, the XRP can go very fast on straight aways and take tight turns with remote control, whereas the classic controlled XRP has to move slower to avoid collisions with the wall. 

2. Humans error can lead to innconsistent results with remote control application:
As shown in our video, it is difficult to control the XRP with the xbox controller without activiely following behind the XRP. THe perspective from a fixed position makes in much harder to determine what inputs to give the xbox controller. This is because the turning behavior of our remote control algorithm make relative turns based on the joy stick and not absolute turns. This difficulty leads to inconsistent robot behavior during the laps. On the contrary, the classic controller has the same decision making criterion regardless of where it is with respective to the lap. This consistency is an advantage of classic control. 

Something we did not test was the fatigue of a human user driving around the track. There are likely additional benefits with classic control over remote control in such conditions. 

3. Without data cleaning and feature engineering, ML models are effectively useless:
While we did take percausion on what data we gave our model (e.g. median filter of the distance sensor), there is still clearly some invalid data within our sets. Occasional faulty encoder reads could easily be skewing our model. Additionally, we did not experiement with what data we actually gave our model. In hindsight, encoder counts alone does not seem to be a revelant datapoint for the model to make preditions on efforts. The efforts produced by the model are almost always outside the -1 to 1 range that the motor requries. It is clear this model is not inteligently calculating motor efforts to navigate the track. 

Suprisingly, the model does seems to have caught on that the average velocity of the outter wheel is larger than the inner wheel. The right wheel efforts are always much larger than the left wheel efforts. We take this as sign that creating a model to complete the track is possible in the future with a better emphacise on ML practices. Regardless of the succcess of our ML, we learned a lot about the process, and will be able to apply this knowledge in the future. 

