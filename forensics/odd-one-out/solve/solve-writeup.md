### Required Tools
- Volatility 3
- CyberChef (optional)

User will first download and extract challenge archive. The archive contains the memory dump of the system and an Intermediate Symbol File (ISF) which is required to read the memory dump properly.

User will then use volatility to list processes and their command line arguments. This can be done by defining the directory where the ISF file is stored,

`vol -s <DIR_OF_ISF> -f <MEM_DUMP> linux.psaux`

This will output the list of processes and their arguments at the time of the memory dump. Amongst the processes, there will be a process listed as kworker. This process is different from other kworker process because the Parent Process ID (PPID) will not be 2, which is the PPID for other kworker processes. In addition, this will be the only kworker process with a command line argument (specifically --token)

```
...
618	2	kworker/u16:4	[kworker/u16:4]
623	2	kworker/u16:5	[kworker/u16:5]
627	1	agetty	/sbin/agetty -o -- \u --noreset --noclear - linux
630	1	sshd	sshd: /usr/sbin/ss
635	2	kworker/R-cfg80	[kworker/R-cfg80]
646	599	dhcpcd	dhcpcd: [DHCP
647	599	dhcpcd	dhcpcd: [BPF
666	599	dhcpcd	dhcpcd: [BOOT
704	630	sshd-session	sshd-session: boss [priv]
709	2	psimon	[psimon]
711	1	systemd	/usr/lib/systemd/systemd --user
713	711	(sd-pam)	(sd-pam)
726	704	sshd-session	sshd-session: boss@pts/0
727	726	bash	-bash
738	727	kworker	[kworker/3:2] --token=ZnRncnB1e2EzM3F5cl8xYV9uX3VubGZnbnB4fQ
746	2	kworker/0:0	[kworker/0:0]
```

Once the user notices the suspicious process, they may analyze the string passed in the token argument. Initially, the string looks encoded. The user can run the magic tool on CyberChef to analyze the string. This will result in output that looks similar to what the flag would look like, but is still illegible. User can then attempt different ciphers until they attempt ROT13 which should give them the flag.

```ZnRncnB1e2EzM3F5cl8xYV9uX3VubGZnbnB4fQ ---> Magic ---> From Base64 ---> ftgrpu{a33qyr_1a_n_unlfgnpx} ---> sgtech{n33dle_1n_a_haystack}```

