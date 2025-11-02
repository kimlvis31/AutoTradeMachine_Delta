# AutoTradeMachine_Delta

This is the fourth version of the **Auto Trade Machine** project.

The main aspects of this version are:
- **Various GUI object & page setup method tests**
- **GUI concepts testing**
- **IPC module implementation & performance testing**
- **(REMOVED) login page (Decided it is better without it at the moment)**

Out of all the previous versions of ATM project, this one has the most experimental nature.

***IPC (Inter-Process Communication)***
The main reason why this project is designed to be a multi-process application is that each of the processes (GUI, API Interaction, Data Management, Analysis, etc.) is expected to be computationally intensive.
Since different processes have their own memory space, a process cannot directly access the data that's being processed by another. To do so, the data needs to be handled on or transferred via shared-memory space or kernel. 
There are many ways to achieve this, but there are more ways to achieve this *inefficiently*. One way would be to transfer data from one process to another via kernel, but my decision at the time was that using shared memory as a buffer was the best, since Python provides easy-to-use library tools to transfer Python-objects via shared memory. 
IPC module implemented in this version was the first attempt to create a reliable and portable IPC module for this project. Even though it still had its limitations and room for improvement at the end, it was a great stepping stone.

***GUI***
GUI design can be neck-breaking. Implementing it is more so. Having no experience in the field, I had no sense of how to efficiently update and maintain what is to become a large GUI platform. I could just look at what others do, but I also wanted to come up with my own idea and learn from my own failures. In this version, I attempt to design a GUI *page* and store its metadata in text files. Upon application launch, the text files are loaded and GUI objects are initialized accordingly. I would like to think this was the first time I started gaining some sense of *configuration* file management.

---

### 🗓️ Project Duration
**September 2023 – October 2023**

---

### 📄 Document Info
**Last Updated:** November 3rd, 2025  
**Author:** Bumsu Kim  
**Email:**  kimlvis31@gmail.com  
