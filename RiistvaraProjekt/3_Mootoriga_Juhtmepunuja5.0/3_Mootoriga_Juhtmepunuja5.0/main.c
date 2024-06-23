/*
 * 3_Mootoriga_Juhtmepunuja2.0.c
 *
 * Created: 08.02.2024 20:41:28
 * Author : ralfs
 */ 

#include <avr/io.h>
#include <util/delay.h>
#include <compat/twi.h>
#include <stdbool.h>
#include <avr/interrupt.h>

#define F_CPU 16000000UL  // Assuming a 16MHz clock
#define F_SCL 100000UL    // 100kHz I2C clock
#define TWBR_val ((((F_CPU / F_SCL) / 1) - 16) / 2)

// LCD commands
#define LCD_CLEARDISPLAY 0x01
#define LCD_RETURNHOME 0x02
#define LCD_ENTRYMODESET 0x04
#define LCD_DISPLAYCONTROL 0x08
#define LCD_CURSORSHIFT 0x10
#define LCD_FUNCTIONSET 0x20
#define LCD_SETCGRAMADDR 0x40
#define LCD_SETDDRAMADDR 0x80
#define MAX_LINE_LENGTH 16  // LCD rea pikkus


// Flags for display on/off control
#define LCD_DISPLAYON 0x04
#define LCD_DISPLAYOFF 0x00
#define LCD_CURSORON 0x02
#define LCD_CURSOROFF 0x00
#define LCD_BLINKON 0x01
#define LCD_BLINKOFF 0x00

// State machine
#define STATE_SELECTING_DIAMETER 0
#define STATE_SELECTING_LENGTH 1
#define STATE_READY_TO_START 2
#define STATE_RUNNING 3

// I2C address for the LCD
#define LCD_ADDRESS (0x27 << 1)  // Adjust as per your LCD's address

void i2c_init(void) {
	TWSR = 0;
	TWBR = (uint8_t)TWBR_val;
}

uint8_t i2c_start(uint8_t address) {
	TWCR = 0;
	TWCR = (1 << TWSTA) | (1 << TWEN) | (1 << TWINT);
	while (!(TWCR & (1 << TWINT)));
	
	if ((TWSR & 0xF8) != TW_START) { return 1; }
	
	TWDR = address;
	TWCR = (1 << TWEN) | (1 << TWINT);
	while (!(TWCR & (1 << TWINT)));
	
	uint8_t twst = TW_STATUS & 0xF8;
	if ((twst != TW_MT_SLA_ACK) && (twst != TW_MR_SLA_ACK)) return 1;
	
	return 0;
}

void i2c_stop(void) {
	TWCR = (1 << TWSTO) | (1 << TWEN) | (1 << TWINT);
	while(TWCR & (1 << TWSTO));
}

uint8_t i2c_write(uint8_t data) {
	TWDR = data;
	TWCR = (1 << TWINT) | (1 << TWEN);
	while (!(TWCR & (1 << TWINT)));
	
	if ((TWSR & 0xF8) != TW_MT_DATA_ACK) { return 1; }
	
	return 0;
}

void lcd_send_cmd(uint8_t cmd) {
	uint8_t data_u, data_l;
	uint8_t data_t[4];
	data_u = (cmd & 0xf0);
	data_l = ((cmd << 4) & 0xf0);
	data_t[0] = data_u | 0x0C;  // en=1, rs=0
	data_t[1] = data_u | 0x08;  // en=0, rs=0
	data_t[2] = data_l | 0x0C;  // en=1, rs=0
	data_t[3] = data_l | 0x08;  // en=0, rs=0

	i2c_start(LCD_ADDRESS | TW_WRITE);
	for (int i = 0; i < 4; i++) {
		i2c_write(data_t[i]);
	}
	i2c_stop();
}

void lcd_send_data(uint8_t data) {
	uint8_t data_u, data_l;
	uint8_t data_t[4];
	data_u = (data & 0xf0);
	data_l = ((data << 4) & 0xf0);
	data_t[0] = data_u | 0x0D;  // en=1, rs=1
	data_t[1] = data_u | 0x09;  // en=0, rs=1
	data_t[2] = data_l | 0x0D;  // en=1, rs=1
	data_t[3] = data_l | 0x09;  // en=0, rs=1

	i2c_start(LCD_ADDRESS | TW_WRITE);
	for (int i = 0; i < 4; i++) {
		i2c_write(data_t[i]);
	}
	i2c_stop();
}

void lcd_init(void) {
	lcd_send_cmd(0x02);  // Initialize the LCD in 4-bit mode
	lcd_send_cmd(0x28);  // 2 lines and 5x7 matrix
	lcd_send_cmd(0x0c);  // display on, cursor off
	lcd_send_cmd(0x80);  // force cursor to beginning of the first line
}

void lcd_set_cursor(int row, int col) {
	const uint8_t offsets[] = { 0x00, 0x40 };
	lcd_send_cmd(LCD_SETDDRAMADDR | (offsets[row] + col));
}

void lcd_write_text_wrapped(const char* text) {
	int i = 0;
	lcd_set_cursor(0, 0);  // Alusta esimesest reast

	while (text[i] != '\0' && i < MAX_LINE_LENGTH) {
		lcd_send_data(text[i]);
		i++;
	}

	if (text[i] != '\0') {
		lcd_set_cursor(1, 0);  // Jätka teisest reast
		while (text[i] != '\0') {
			lcd_send_data(text[i]);
			i++;
		}
	}
}


void update_lcd_diameter(float diameter) {
	char message[40];
	int diameterTenths = (int)(diameter * 10);  // Convert to tenths of mm
	sprintf(message, "Wire diameter: %d.%dmm", diameterTenths / 10, diameterTenths % 10);
	lcd_send_cmd(LCD_CLEARDISPLAY);
	lcd_write_text_wrapped(message);
}

void update_lcd_countdown(int time) {
	char message[40];
	if (time < 10) {
		sprintf(message, "Time left: %d", time);
		} else {
		sprintf(message, "Time left: %d", time);
	}
	lcd_send_cmd(LCD_CLEARDISPLAY); // Clear the display for the new message
	lcd_write_text_wrapped(message); // Write the formatted countdown time to the LCD
}

void update_lcd_length(int length) {
	char message[40];
	sprintf(message, "Wire length: %dcm", length);
	lcd_send_cmd(LCD_CLEARDISPLAY);
	lcd_write_text_wrapped(message);
}

void update_lcd_ready_to_start() {
	lcd_send_cmd(LCD_CLEARDISPLAY);
	lcd_write_text_wrapped("Ready! Press S2 to start.");
}

// Button setup for S2 (PF7)
#define BUTTON_S2_PIN PINF7
#define BUTTON_S2_PORT PINF
#define BUTTON_S2_DDR DDRF
#define BUTTON_S2_PRESSED !(BUTTON_S2_PORT & (1 << BUTTON_S2_PIN))

// Button setup for S3 (PB0)
#define BUTTON_S3_PIN PINB0
#define BUTTON_S3_PORT PINB
#define BUTTON_S3_DDR DDRB
#define BUTTON_S3_PRESSED !(BUTTON_S3_PORT & (1 << BUTTON_S3_PIN))

// Button setup for S4 (PD5)
#define BUTTON_S4_PIN PIND5
#define BUTTON_S4_PORT PIND
#define BUTTON_S4_DDR DDRD
#define BUTTON_S4_PRESSED !(BUTTON_S4_PORT & (1 << BUTTON_S4_PIN))

// Motor1 control pins
#define STEP_PIN1 PINE6
#define DIR_PIN1 PINC7
#define MOTOR_CONTROL_ADDITIONAL_PIN1 PIND7

#define MOTOR_CONTROL_DDRE DDRE
#define MOTOR_CONTROL_DDRC DDRC

#define MOTOR_CONTROL_PORT1 PORTE
#define MOTOR_CONTROL_PORT2 PORTC

// Motor2 control pins
#define STEP_PIN2 PIND6
#define DIR_PIN2 PIND4
#define MOTOR_CONTROL_ADDITIONAL_PIN2 PIND2
#define MOTOR_CONTROL_DDR DDRD  // Both pins are on PORTD
#define MOTOR_CONTROL_PORT PORTD

// Motor3 control pins
#define STEP_PIN3 PINB7
#define DIR_PIN3 PINB6
#define MOTOR_CONTROL_ADDITIONAL_PIN3 PINB4
#define MOTOR_CONTROL_DDR3 DDRB
#define MOTOR_CONTROL_PORT3 PORTB


void setup_button_s2() {
	BUTTON_S2_DDR &= ~(1 << BUTTON_S2_PIN);  // Set PF7 as input
	// Optionally enable pull-up resistor if your button setup needs it
	// BUTTON_S2_PORT |= (1 << BUTTON_S2_PIN);
}

void setup_button_s3() {
	BUTTON_S3_DDR &= ~(1 << BUTTON_S3_PIN);  // Set PB0 as input
	// Optionally enable pull-up resistor if your button setup needs it
	// BUTTON_S3_PORT |= (1 << BUTTON_S3_PIN);
}

void setup_button_s4() {
	BUTTON_S4_DDR &= ~(1 << BUTTON_S4_PIN);  // Set PD5 as input
	// Optionally enable pull-up resistor if your button setup needs it
	// BUTTON_S4_PORT |= (1 << BUTTON_S4_PIN);
}


void setup_motor_pins() {
	//Mootor1 omad
	// Set STEP pin (PE6) as output
	DDRE |= (1 << STEP_PIN1);
	// Initialize STEP pin to low
	PORTE &= ~(1 << STEP_PIN1);

	// Set DIR pin (PC7) as output
	DDRC |= (1 << DIR_PIN1);
	// Initialize DIR pin to low
	PORTC &= ~(1 << DIR_PIN1);

	// Set the additional motor control pin (PIND7) as output
	DDRD |= (1 << MOTOR_CONTROL_ADDITIONAL_PIN1);
	// Initialize the additional motor control pin to low
	PORTD &= ~(1 << MOTOR_CONTROL_ADDITIONAL_PIN1);
	
	//Mootor2 omad
	MOTOR_CONTROL_DDR |= (1 << STEP_PIN2) | (1 << DIR_PIN2);  // Set STEP and DIR pins as output
	MOTOR_CONTROL_PORT &= ~((1 << STEP_PIN2) | (1 << DIR_PIN2));  // Initialize pins to low
	
	//Mootor3 omad
	// Set STEP and DIR pins as output for Motor3
	MOTOR_CONTROL_DDR3 |= (1 << STEP_PIN3) | (1 << DIR_PIN3);
	/// Set the DIR pin high to reverse the motor direction
	MOTOR_CONTROL_PORT3 |= (1 << DIR_PIN3);
	// Initialize STEP pin to low
	MOTOR_CONTROL_PORT3 &= ~(1 << STEP_PIN3);
	// Set the additional motor control pin for Motor3 as output
	DDRB |= (1 << MOTOR_CONTROL_ADDITIONAL_PIN3);
	// Initialize the additional motor control pin to low
	PORTB &= ~(1 << MOTOR_CONTROL_ADDITIONAL_PIN3);
}

//volatile uint16_t CurrentState = 0;

// Global variables to control stepping intervals for each motor
volatile uint16_t interval1 = 0, interval2 = 0, interval3 = 0;

// Declare global variables for motor control
volatile uint16_t motor1Counter = 0, motor2Counter = 0, motor3Counter = 0;

// Declare very budget realtime countdown.
volatile int16_t Countdown = 0;
volatile uint16_t TimetoReach = 0;
volatile uint16_t StartTime = 0;
volatile bool StopTime = false;

void setup_timer1() {
	TCCR1A = 0; // Set Timer1 to CTC mode
	TCCR1B = 0;
	//TCCR1B = (1 << WGM12) | (1 << CS11); // CTC mode, prescaler 8
	TCCR1B |= (1 << WGM12) | (1 << CS11) | (1 << CS10);
	TCNT1 = 0;
	OCR1A = 40; // Compare value for base stepping rate, adjust as needed
	sei();
}

ISR(TIMER1_COMPA_vect) {
	PORTF ^= (1 << PINF4); // debug red LED
	interval1++;
	interval2++;
	interval3++;
	if (motor1Counter <= interval1){
	PORTE ^= (1 << STEP_PIN1); // Toggle step pin for Motor 1
	interval1 = 0;
	}
	if (motor2Counter <= interval2){
	MOTOR_CONTROL_PORT ^= (1 << STEP_PIN2); // Toggle step pin for Motor 2
	interval2 = 0;
	}
	if (motor3Counter <= interval3){
	MOTOR_CONTROL_PORT3 ^= (1 << STEP_PIN3); // Toggle step pin for Motor 3
	interval3 = 0;
	}
}

void setup_timer3() {
	TCCR3A = 0; // Ensure Control Register A is set to zero
	TCCR3B = 0; // Reset Control Register B
	
	// Configure Timer3 for CTC mode with a prescaler
	// Example: Set CTC mode (WGM32 = 1) and prescaler (CS31 and CS30 for prescaler 64)
	TCCR3B |= (1 << WGM32) | (1 << CS31) | (1 << CS30);
	
	// Initialize Timer3 counter to zero
	TCNT3 = 0;
	
	// Set the Output Compare Register 3A (OCR3A)
	// This value determines the timer's top value and, consequently, its frequency
	OCR3A = 28200; // Example for a 1s interval at 16MHz clock with prescaler 64
	//28235 APROX SEKUND
	// Enable Timer3 Compare A Match interrupt
}

ISR(TIMER3_COMPA_vect) {
	// Toggle an LED or perform another task
	// Example: Toggle a pin on PORTC
	//PORTC ^= (1 << PC7); // Assuming you have an LED connected to PC7
 // Enable Timer1 Compare A Match interrupt
	Countdown -= 1;
}


void start_motors(uint16_t speed1, uint16_t speed2, uint16_t speed3) {
	// Set target steps and speed for each motor
	motor1Counter = (100-speed1);
	motor2Counter = (100-speed2);
	motor3Counter = (100-speed3);

	// Activate additional control pins if necessary, for example, enable drivers
	// Motor 1
	MOTOR_CONTROL_PORT |= (1 << MOTOR_CONTROL_ADDITIONAL_PIN1);  // Activate additional control pin for the first motor

	// Motor 2
	// Adjust PORTx and MOTOR_CONTROL_ADDITIONAL_PIN2 to match your setup
	PORTD |= (1 << MOTOR_CONTROL_ADDITIONAL_PIN2);  // Activate additional control pin for the second motor

	// Motor 3
	// Adjust PORTy and MOTOR_CONTROL_ADDITIONAL_PIN3 to match your setup
	PORTB |= (1 << MOTOR_CONTROL_ADDITIONAL_PIN3);  // Activate additional control pin for the third motor

}

void disable_JTAG(void) {
	MCUCR |= (1 << JTD);
	MCUCR |= (1 << JTD);
}

int main(void) {
	disable_JTAG();  // Disable JTAG interface
	i2c_init();  // Initialize I2C
	lcd_init();  // Initialize LCD
	setup_button_s2(); // Initialize button S2
	setup_button_s4();  // Initialize button S4
	setup_motor_pins();  // Initialize motor control pins
	setup_timer1(); // For motors
	setup_timer3(); // For time

	float wireDiameter = 0.1f;  // Starting diameter
	int wireLength = 10;  // Starting length in cm

	update_lcd_diameter(wireDiameter);  // Initial LCD update
	uint8_t CurrentState = STATE_SELECTING_DIAMETER;
	
	// Set PF4 as an output
	DDRF |= (1 << PF4);


	while (1) {
		//update_lcd_diameter(wireDiameter);  // Initial LCD update
		_delay_ms(50); // Debouncing delay
		if (CurrentState == STATE_RUNNING){
			uint16_t Countersmol = 0;
			//CurrentState = STATE_SELECTING_DIAMETER;
			while (StopTime == false) {
				if (Countersmol > 100) {
					update_lcd_countdown(Countdown);
					Countersmol = 0;
				} else {
					_delay_ms(3);
					Countersmol++;;
				}	
				if (Countdown <= 0) {
					CurrentState = STATE_SELECTING_DIAMETER;
					TIMSK3 = (0 << OCIE3A);
					TIMSK1 = (0 << OCIE1A);
					StopTime = true;
				}
			}
			CurrentState = STATE_SELECTING_DIAMETER;
			update_lcd_diameter(wireDiameter);  // Initial LCD update
		}
		if (BUTTON_S4_PRESSED) {
			_delay_ms(200); // Delay for button debounce
			if (CurrentState == STATE_SELECTING_DIAMETER) {
				wireDiameter += 0.1f;
				if (wireDiameter > 2.5f) wireDiameter = 0.1f;  // Wrap around
				update_lcd_diameter(wireDiameter);
				} else if (CurrentState == STATE_SELECTING_LENGTH) {
				wireLength += 10;
				if (wireLength > 200) wireLength = 10;  // Wrap around
				update_lcd_length(wireLength);
			}
			// No action for STATE_READY_TO_START when S4 is pressed
		}

		if (BUTTON_S2_PRESSED) {
			_delay_ms(200); // Delay for button debounce
			if (CurrentState == STATE_SELECTING_DIAMETER) {
				CurrentState = STATE_SELECTING_LENGTH;  // Move to selecting length
				update_lcd_length(wireLength);
				} else if (CurrentState == STATE_SELECTING_LENGTH) {
				CurrentState = STATE_READY_TO_START;  // Ready to start
				update_lcd_ready_to_start();
				} else if (CurrentState == STATE_READY_TO_START) {
				// Start motor operation with selected diameter and length
				//operate_motor_with(wireDiameter, wireLength);
				//_delay_ms(58000); / 30sek
				//TimetoReach = 20;
				Countdown = 5;
				StartTime = 0;
				start_motors(100, 50, 0); // Example call
				TIMSK3 = (1 << OCIE3A);
				TIMSK1 = (1 << OCIE1A);
				sei();
				// Optionally, reset to initial state after operation
				//CurrentState = STATE_SELECTING_DIAMETER;
				wireDiameter = 0.1f;  // Reset diameter
				wireLength = 10;  // Reset length
				CurrentState = STATE_RUNNING;
				//update_lcd_diameter(wireDiameter);
			}
		}
		
	}
}

