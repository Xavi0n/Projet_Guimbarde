/*
 * @file rc_test_servos.c
 * @example    rc_test_servos
 *
 * @author     James Strawson
 * @date       3/20/2018
 */

#include <signal.h>
#ifdef __arm__
// BeagleBone target platform
#include "time.h"
#include "servo.h"
#else
// Development platform
#include "../dev_includes/beaglebone_stubs.h"
#endif
#include "ServoAdjust.h"
#include "main.h"


int Servo_Movements(void)
{
	// initialize PRU
	if(rc_servo_init()) {
		return -1;
	}

	while(running)
	{
		vmoveTurretHorizontal(current_horizontal_angle);
		vmoveTurretVertical(current_vertical_angle);
		rc_usleep(1000000/50);
	}

	rc_usleep(50000);
	rc_servo_cleanup();
	return 0;
}

void vmoveTurretHorizontal(int angle)
{
	if(angle <= 110 && angle >= 0)
	{
		static double AngleServo = 55;
		double sweep_limitH = angle;
		int directionH = 0;
		double Servo_positionH;

		if(AngleServo < sweep_limitH)
		{
			directionH = 2;
			AngleServo += 1.0 * sweep_limitH / 50.0;
		}
		if(AngleServo > sweep_limitH)
		{
			directionH = -2;
			AngleServo += -1.0 * sweep_limitH / 50.0;
		}

		if(AngleServo > sweep_limitH && directionH == 1)
		{
			AngleServo = sweep_limitH;
			directionH = 0;
		}
		else if(AngleServo < sweep_limitH && directionH == -1)
		{
			AngleServo = sweep_limitH;
			directionH = 0;
		}
		Servo_positionH = ((AngleServo / 270.0) * 3.0) - 1.5;
		
		rc_servo_send_pulse_normalized(1, Servo_positionH);
	}
}

void vmoveTurretVertical(int angle)
{
	if(angle <= 160 && angle >= 55)
	{
		static double AngleServo = 10;
		double sweep_limitV = angle;
		int directionV = 0;
		double Servo_positionV;

		if(AngleServo < sweep_limitV)
		{
			directionV = 2;
			AngleServo += 1.0 * sweep_limitV / 50.0;
		}
		if(AngleServo > sweep_limitV)
		{
			directionV = -2;
			AngleServo += -1.0 * sweep_limitV / 50.0;
		}

		if(AngleServo > sweep_limitV && directionV == 1)
		{
			AngleServo = sweep_limitV;
			directionV = 0;
		}
		else if(AngleServo < sweep_limitV && directionV == -1)
		{
			AngleServo = sweep_limitV;
			directionV = 0;
		}
		Servo_positionV = ((AngleServo / 270.0) * 3.0) - 1.5;

		rc_servo_send_pulse_normalized(2, Servo_positionV);
		// Inverse of the other servo
		rc_servo_send_pulse_normalized(3, -Servo_positionV);
	}
}
