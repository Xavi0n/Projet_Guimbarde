#ifndef SERVOADJUST_H
#define SERVOADJUST_H

/**
 * Initialize and run the servo movement loop
 * @return 0 on success, -1 on error
 */
int Servo_Movements(void);

/**
 * Move the horizontal turret servo to a specific angle
 * @param angle Target angle (0-110 degrees)
 */
void vmoveTurretHorizontal(int angle);

/**
 * Move the vertical turret servos to a specific angle
 * @param angle Target angle (10-160 degrees)
 */
void vmoveTurretVertical(int angle);

#endif
