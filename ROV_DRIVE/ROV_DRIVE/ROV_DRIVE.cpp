/******************************************************************************\
UNH UNDERWATER ROV DRIVE CONTROLS

This code reads in controller input (XBox 360 controller) and passes along values to an arduino.
This particular code was developed and modified for the control of ROV-004 during the summer 
of 2015. There is no leap motion controls in this code and the ROV is only controlled by the 
controller and the arduino code that has feedback control.


Code originally by Nate Cordova and Alex Sarasin
Edited code by Shawn Swist

\******************************************************************************/
#include "stdafx.h"
#include "rov_drive_h.h"


 #ifdef USE_DIRECTX_SDK
#include <C:\Program Files (x86)\Microsoft DirectX SDK (June 2010)\include\xinput.h>
#pragma comment(lib,"xinput.lib")
#elif (_WIN32_WINNT >= 0x0602 /*_WIN32_WINNT_WIN8*/)
#include <XInput.h>
#pragma comment(lib,"xinput.lib")
#else
#include <XInput.h>
#pragma comment(lib,"xinput9_1_0.lib")
#endif


//-----------------------------------------------------------------------------
// Defines, constants, and global variables
//-----------------------------------------------------------------------------
#define MAX_CONTROLLERS 4  // XInput handles up to 4 controllers 
#define CONTROLLER_DEADZONE  ( 0.15f * FLOAT(0x7FFF) )  // Default to 24% of the +/- 32767 range.   This is a reasonable default value but can be altered if needed.
#define CONTROLLER1 0
#define NUMBER_OF_BUTTONS 20

//#define NUMBER_OF_LEAP_INPUTS 7
//#define LEAP_DEADZONE 50

CSerial SerialPort;

struct CONTROLLER_STATE
{
	XINPUT_STATE state;
	bool bConnected;
};

CONTROLLER_STATE g_Controllers[MAX_CONTROLLERS];
ControllerInput Controller[NUMBER_OF_BUTTONS + 1];
WCHAR g_szMessage[4][1024] = { 0 };
HWND    g_hWnd;
bool    g_bDeadZoneOn = true;


char recieved[20][20];

int main()
{

	unsigned long cycles = 0;


	int i = 0;

	// ********************************************************************************************************************
	// IMPORTANT: The serial port numbers here must correspond to those of the arduino on the ROV. The first number is the 
	// COM # and the second number is the baud rate set on the arduino.
	SerialPort.Open(8, 115200);
	// ********************************************************************************************************************

	Controller[20].value = 9;	//Verification Byte sent to make sure everything else ends up in the right location
	FillByteSize();

	while (true)
	{
		cycles++;
		UpdateControllerState();	//Updates all values on the controller
		WORD wButtons = g_Controllers[CONTROLLER1].state.Gamepad.wButtons;

		//Stores all of the values from the controller into the controller structure
		Controller[0].value = g_Controllers[CONTROLLER1].state.Gamepad.sThumbRX;
		Controller[1].value = g_Controllers[CONTROLLER1].state.Gamepad.sThumbRY;
		Controller[2].value = g_Controllers[CONTROLLER1].state.Gamepad.sThumbLX;
		Controller[3].value = g_Controllers[CONTROLLER1].state.Gamepad.sThumbLY;
		Controller[4].value = (g_Controllers[CONTROLLER1].state.Gamepad.bRightTrigger);
		Controller[5].value = (g_Controllers[CONTROLLER1].state.Gamepad.bLeftTrigger);
		Controller[6].value = (wButtons & XINPUT_GAMEPAD_RIGHT_THUMB);
		Controller[7].value = (wButtons & XINPUT_GAMEPAD_LEFT_THUMB);
		Controller[8].value = (wButtons & XINPUT_GAMEPAD_RIGHT_SHOULDER);
		Controller[9].value = (wButtons & XINPUT_GAMEPAD_LEFT_SHOULDER);
		Controller[10].value = (wButtons & XINPUT_GAMEPAD_DPAD_UP);
		Controller[11].value = (wButtons & XINPUT_GAMEPAD_DPAD_DOWN);
		Controller[12].value = (wButtons & XINPUT_GAMEPAD_DPAD_LEFT);
		Controller[13].value = (wButtons & XINPUT_GAMEPAD_DPAD_RIGHT);
		Controller[14].value = (wButtons & XINPUT_GAMEPAD_A);
		Controller[15].value = (wButtons & XINPUT_GAMEPAD_B);
		Controller[16].value = (wButtons & XINPUT_GAMEPAD_Y);
		Controller[17].value = (wButtons & XINPUT_GAMEPAD_X);
		Controller[18].value = (wButtons & XINPUT_GAMEPAD_START);
		Controller[19].value = (wButtons & XINPUT_GAMEPAD_BACK);

		CheckDeadZone();
		

		for (i = 6; i < NUMBER_OF_BUTTONS; i++)	//DO NOT SET TO <= NUMBER_OF_BUTTONS, NOT A MISTAKE. Verification bit should always keep its value
		{
			{
				Controller[i].value = AnalogToDigital(Controller[i].value);	//converts all of the button presses on the controller to a binary value
			}
		}

		//turns all of the numerical values into buffers that can be passed to the arduino
		for (i = 0; i <= NUMBER_OF_BUTTONS; i++)
		{
			_itoa_s(Controller[i].value, Controller[i].passedValue, 10);
		}

		
		if (SendData() == 1)
		{
			//SerialPort.ReadData(recieved[0], 3);
		}

		std::cout << Controller[5].value << Controller[4].value << Controller[1].value << std::endl;  // This shows the value being passed to the arduino from the selected controller button (#3 = Left stick Y position)
		
	}
	return 0;
}

//-----------------------------------------------------------------------------
HRESULT UpdateControllerState()
{
	DWORD dwResult;
	for (DWORD w = 0; w < MAX_CONTROLLERS; w++)
	{
		// Simply get the state of the controller from XInput.
		dwResult = XInputGetState(w, &g_Controllers[w].state);

		if (dwResult == ERROR_SUCCESS)
			g_Controllers[w].bConnected = true;
		else
			g_Controllers[w].bConnected = false;
	}

	return S_OK;
}

//Defaulty, each controller button has its own respective value for high when pressed.
//Analog to digital converts them all to a binary value so less data needs to be sent to the arduino
int AnalogToDigital(int ControllerVal)
{
	if (ControllerVal != 0)
	{
		return 1;
	}

	else
		return 0;
}

//Tells the structure what the packet size should be for each piece of data
//analog sticks need 7 bytes, triggers take 4, buttons take 2
void FillByteSize()
{
	int i = 0;
	for (i = 0; i <= NUMBER_OF_BUTTONS; i++)
	{
		if (i <= 3)
			Controller[i].packetSize = 7;

		if (i >= 4 && i <= 5)
			Controller[i].packetSize = 4;

		if (i >= 6 && i <= NUMBER_OF_BUTTONS)
		{
			Controller[i].packetSize = 2;
		}
	}
	
}


//Checks the value to the analog sticks and converts them to zero if they are under the threshold
void CheckDeadZone()
{
	int i = 0;
	for (i = 0; i <= 3; i++)
	{
		if (abs(Controller[i].value) < CONTROLLER_DEADZONE)
		{
			Controller[i].value = 0;
		}
	}
}


int SendData()
{
	int i = 0;
	int count = 0;
	char ioControlBuffer[3];
	char ioControl[3];
	int bytesRecieved = 0;
	SerialPort.SendData("hgl", 3);

	while (true)
	{
		bytesRecieved = SerialPort.ReadData(ioControlBuffer, 1);

		ioControl[0] = ioControlBuffer[0];
		printf("%c\t%d\t", ioControlBuffer[0], bytesRecieved);
		


	   if (ioControl[0] == 'r')
		{
			for (i = 0; i <= NUMBER_OF_BUTTONS; i++)
				SerialPort.SendData(Controller[i].passedValue, sizeof(Controller[i].passedValue));
			
			count++;
			if (count > 5)
			{
				Sleep(750);
				return 0;
			}
		}

		else if (ioControl[0] == 'q')
		{
			return 1;
		}

		else
		{
			printf("Error: Unknown codeword passed from arduino [%c], aborting send\n", ioControl[0]);
		}
		
	}
}