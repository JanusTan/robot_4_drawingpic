clear all;
 % port at which your arduino is connected
 port = 'COM9';
% model arduino board
 board = 'Mega2560';
% creating arduino object with servo librarytheta2
 arduino_board = arduino(port, board, 'Libraries', 'Servo');
% creating servo motor object
    servo_motor1 = servo(arduino_board, 'D9');
    servo_motor2 = servo(arduino_board, 'D7');
    servo_motor3 = servo(arduino_board, 'D6');
    theta3 = 0.63;
    theta4 = 0.4;
    L1=145;
   L2=125;
   fid=fopen('dola1.nc');  


while ~feof(fid)

 str = fgetl(fid);   
 if ((str(1)=='G')&&(str(2)=='1'))||((str(1)=='G')&&(str(2)=='0'))
   data=regexp(str,'\d*\.?\d*','match');
   a=data{2};
   b=data{3};
   X=str2double(a);
   Y=str2double(b);
      disp([X,Y]);
   plot(X,Y,'.');
   axis([10 200 10 200]);
   hold on;
   theta2 = (acos((X^2+Y^2-L1^2-L2^2)/(2*L1*L2)))*(1/180)*(180/pi);
   theta1 = (atan(Y/X)-atan((L2*sin(theta2))/(L1+L2*cos(theta2))))*(1/180)*(180/pi);
   writePosition(servo_motor1, theta1);
   writePosition(servo_motor2, theta2); 
   pause(0.01);
 end
 if (str(1)=='M')&&(str(2)=='3')
     writePosition(servo_motor3, theta3);
     pause(0.5);
 end
 if ((str(1)=='M')&&(str(2)=='5'))||((str(1)=='G')&&(str(2)=='9'))
     writePosition(servo_motor3, theta4);
     pause(0.5);
 end
end

