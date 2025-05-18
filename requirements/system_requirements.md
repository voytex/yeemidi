# System Requirements

| Req. ID | Definition |
|:-------:|:----------|
| `sys-1` | Application shall provide functionality to control Yeelight RGB Bulbs using MIDI (mainly from SW loopback bus). Particular MIDI messages and their effect shall be discussed in separate document. |
| `sys-2` | Application shall be able to control Yeelight bulbs connected to the same local area network as the computer that runs this application. |
| `sys-3` | Application shall be able to distinguish bulbs based on their __unique ID__ and shall not rely on IP addresses. |
| `sys-4` | Application shall be able to group bulbs. Bulbs in a single group shall receive commands ideally at the same time. |
| `sys-5` | Application shall provide functionality for 'sound check' mode where only particular bulbs or bulbs from a particular group would light up to be positioned in the venue space correctly. |

