// CONFIG1H
#pragma config OSC = HS         // Oscillator Selection bits (HS oscillator)
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor Enable bit (Fail-Safe Clock Monitor disabled)
#pragma config IESO = ON        // Internal/External Oscillator Switchover bit (Oscillator Switchover mode enabled)

// CONFIG2L
#pragma config PWRT = OFF       // Power-up Timer Enable bit (PWRT disabled)
#pragma config BOREN = SBORDIS  // Brown-out Reset Enable bits (Brown-out Reset enabled in hardware only (SBOREN is disabled))
#pragma config BORV = 3         // Brown Out Reset Voltage bits (Minimum setting)

// CONFIG2H
#pragma config WDT = ON         // Watchdog Timer Enable bit (WDT enabled)
#pragma config WDTPS = 32768    // Watchdog Timer Postscale Select bits (1:32768)

// CONFIG3H
#pragma config CCP2MX = PORTC   // CCP2 MUX bit (CCP2 input/output is multiplexed with RC1)
#pragma config PBADEN = ON      // PORTB A/D Enable bit (PORTB<4:0> pins are configured as analog input channels on Reset)
#pragma config LPT1OSC = OFF    // Low-Power Timer1 Oscillator Enable bit (Timer1 configured for higher power operation)
#pragma config MCLRE = ON       // MCLR Pin Enable bit (MCLR pin enabled; RE3 input pin disabled)

// CONFIG4L
#pragma config STVREN = ON      // Stack Full/Underflow Reset Enable bit (Stack full/underflow will cause Reset)
#pragma config LVP = ON         // Single-Supply ICSP Enable bit (Single-Supply ICSP enabled)
#pragma config XINST = OFF      // Extended Instruction Set Enable bit (Instruction set extension and Indexed Addressing mode disabled (Legacy mode))

// CONFIG5L
#pragma config CP0 = OFF        // Code Protection bit (Block 0 (000800-003FFFh) not code-protected)
#pragma config CP1 = OFF        // Code Protection bit (Block 1 (004000-007FFFh) not code-protected)
#pragma config CP2 = OFF        // Code Protection bit (Block 2 (008000-00BFFFh) not code-protected)
#pragma config CP3 = OFF        // Code Protection bit (Block 3 (00C000-00FFFFh) not code-protected)

// CONFIG5H
#pragma config CPB = OFF        // Boot Block Code Protection bit (Boot block (000000-0007FFh) not code-protected)
#pragma config CPD = OFF        // Data EEPROM Code Protection bit (Data EEPROM not code-protected)

// CONFIG6L
#pragma config WRT0 = OFF       // Write Protection bit (Block 0 (000800-003FFFh) not write-protected)
#pragma config WRT1 = OFF       // Write Protection bit (Block 1 (004000-007FFFh) not write-protected)
#pragma config WRT2 = OFF       // Write Protection bit (Block 2 (008000-00BFFFh) not write-protected)
#pragma config WRT3 = OFF       // Write Protection bit (Block 3 (00C000-00FFFFh) not write-protected)

// CONFIG6H
#pragma config WRTC = OFF       // Configuration Register Write Protection bit (Configuration registers (300000-3000FFh) not write-protected)
#pragma config WRTB = OFF       // Boot Block Write Protection bit (Boot Block (000000-0007FFh) not write-protected)
#pragma config WRTD = OFF       // Data EEPROM Write Protection bit (Data EEPROM not write-protected)

// CONFIG7L
#pragma config EBTR0 = OFF      // Table Read Protection bit (Block 0 (000800-003FFFh) not protected from table reads executed in other blocks)
#pragma config EBTR1 = OFF      // Table Read Protection bit (Block 1 (004000-007FFFh) not protected from table reads executed in other blocks)
#pragma config EBTR2 = OFF      // Table Read Protection bit (Block 2 (008000-00BFFFh) not protected from table reads executed in other blocks)
#pragma config EBTR3 = OFF      // Table Read Protection bit (Block 3 (00C000-00FFFFh) not protected from table reads executed in other blocks)

// CONFIG7H
#pragma config EBTRB = OFF      // Boot Block Table Read Protection bit (Boot Block (000000-0007FFh) not protected from table reads executed in other blocks)

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.


#include <xc.h>
#define _XTAL_FREQ 8000000




#include <stdlib.h>
#include <stdio.h>

unsigned char Data, Rdata, TxBuf[16];
int channel;
unsigned char Rec[4];

char * ltoa2(unsigned char *, signed long, int); 
char * ultoa2(char *, unsigned long, int);




uint8_t ThermalValue = 0;
uint8_t ROMcode[8] = {0xab, 0x00, 0x00, 0x00, 0x66, 0x92, 0xcf, 0x42};

void Send(unsigned  char Data)
{
    while(!TXSTAbits.TRMT);
    TXREG   =   Data;
}

void SendASCIIData(unsigned char*TxBuf){
    int numTxData = 0;
    while(1)
    {
        if(TxBuf[numTxData]==0)
        {
            break;
        }
        else
        {
            numTxData=numTxData+1;        
        }
        Send(TxBuf[numTxData-1]);
    }
}

unsigned char Receive(void) 
{
    if(PIR1bits.RCIF)
    {
        PIR1bits.RCIF   =   0;
        if((RCSTAbits.OERR) ||  (RCSTAbits.FERR))
        {
            RCSTA   =   0;
            RCSTA   =   0x90;
            return(0xFF);
        }
        else
            return(RCREG);
    }
    else
        return(0);
}


void WriteToRegister(void)
{
    INTCONbits.INT0IF = 0b0;
    while(INTCONbits.INT0IF == 0b0)
    {
    }
    WriteByteToAdc(0b01000010);
    
    WriteByteToAdc(0b00000001);
    
    WriteByteToAdc(0b00000010);
}

void ResetAdc(void)
{
    int count;
    count ++;
    if(count == 255)
    {
        LATAbits.LA5 = 0b0;
        __delay_us(2);
        LATAbits.LA5 = 0b1;
        WriteToRegister();
    }
}

void ReadData(unsigned char data)
{
    for (int m = 0; m < 8; m++)
    {
        LATCbits.LATC1 = 0b1 ;
        LATBbits.LATB3 = 0b1 ;
        LATBbits.LATB3 = 0b0 ;
        data = data << 1;
        data = data + PORTBbits.RB0;
        LATCbits.LATC1 = 0b0;
    }
}

void convert(void) //24??????????????
{
    char result[16];
    unsigned long adresult;
    signed long pmresult;
    unsigned char DATAMSB = 0x00;
    unsigned char DATAMID = 0x00;   
    unsigned char DATALSB = 0x00;
    
    INTCONbits.INT0IF = 0b0;
    while(INTCONbits.INT0IF == 0b0)
    {
        ResetAdc;
    }
    
    INTCONbits.INT0IF = 0b0;
    while(INTCONbits.INT0IF == 0b0)
    {
    }
    
    ReadData(DATAMSB);
    
    ReadData(DATAMID);
    
    ReadData(DATALSB);
    
    //adresult = (DATAMSB << 16) + (DATAMID <<8) + DATALSB;
    adresult =(unsigned long)DATAMSB * 256UL * 256UL + (unsigned long)DATAMID * 256UL + (unsigned long)DATALSB;
    if((unsigned long)adresult > 8388608UL)
    {
        //LATAbits.LATA1 = 1;
        pmresult = (unsigned long)adresult - 16777216UL;
    }
    else
    {
        pmresult=(unsigned long)adresult;
    }

    //ltoa(result, pmresult, 10);
    //ltoa(result, pmresult, 10);
     ltoa2(result, (signed long)pmresult, 10);

    SendASCIIData(pmresult); 
    //Send('\n');
    /*Send(DATAMSB);
    Send(DATAMID);
    Send(DATALSB);*/
    //Send('\n');
}

void main(void)
{
    OSCCONbits.IRCF2 = 0b1;
    OSCCONbits.IRCF1 = 0b1;
    OSCCONbits.IRCF0 = 0b1;
    OSCCONbits.SCS1 = 0b1;
    OSCCONbits.SCS0 = 0b0;
    INTCONbits.GIE = 0b1;
    INTCONbits.PEIE = 1;
    INTCONbits.INT0IE = 0b1;
    INTCON2bits.INTEDG0 = 0b0;
    TRISA = 0b11000001;
    TRISB = 0b11000101;
    TRISC = 0b10000000;
    TRISD = 0b00000001;
    TRISE = 0b00000000;
    TXSTAbits.TXEN = 0b1;
    TXSTAbits.SYNC = 0b0;
    TXSTAbits.BRGH = 0b1;
    TXSTAbits.TRMT = 0b1;
    RCSTAbits.SPEN = 0b1;
    RCSTAbits.CREN = 0b1;
    BAUDCONbits.BRG16 = 0b1;
    SPBRG = 207;
    ADCON1bits.PCFG = 0b1111;
    LATCbits.LATC1 = 0;
    LATCbits.LATC2 = 0;
    LATCbits.LATC3 = 0;
    LATAbits.LATA5 = 0b1;
    LATCbits.LATC2 = 1;
    WriteToRegister();
    Rdata = 0x00;
    
    while(1)
    {
        Rdata = Receive();
        
        switch (Rdata)
        {
            case 'j':
                Send(Rdata);
                Send('\n');
                LATCbits.LATC3 = 1;
                __delay_ms(500);
                LATCbits.LATC3 = 0;
                break;
                
        }
    }
}