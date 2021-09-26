IMP: Change serial port name as per scanner and zig connection

-> Real-Time Cloud Data Storage
-> Instant Telegram Notification
-> Internet Down Backup and then Upload when network access
-> Local storage enabled
-> Complete logs and Data preview
-> Usually suited for zig and etc PCB testing circuits

Data exchange:
1. Start byte: Serial Data Start Bit from Scanner
2. Message-id: Scanner data
3. CRC: zig data
    if zig pass: upload to cloud with network error backup + local storage
    if zig fail: print circuit not passed, and rescan state
4. Acknowledgment: end bit of zig data

Memory stat:
-> RAM - 21.340 MB
-> VIRTUAL MEMORY - 29.768 MB
-> SHARED LIB MEMORY - 9 MB

External Connect:
-> Serial data external export

Extra Features:
-> AutoStart GUI + terminal
-> Telegram Cloud Integrated
-> Temperature auto shut down
-> 4 modes of operation
Callibrate, DummyTest, ZigTest, Exit