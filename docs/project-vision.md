# なぜ、このプロジェクトを始めたのか / Why I Started This Project

## 日本語

PLC通信ライブラリは、多くの先人たちの努力によって発展してきました。私自身も、その成果に何度も助けられてきました。

一方で、PLCは新しいCPUやEthernetユニット、通信機能が継続的に登場します。OSSとしてそれらに対応し続けることは容易ではなく、実機検証を継続することはさらに大きな負担になります。

私は複数のPLC実機を所有しています。

所有し、問題報告に対して検証可能な機材は、プロトコル別の一覧で公開しています。

- [MELSEC SLMP](https://github.com/fa-yoshinobu/plc-comm-slmp-profiles#verified-hardware-available-for-validation)
- [KEYENCE KV Host Link](https://github.com/fa-yoshinobu/plc-comm-hostlink-profiles#verified-hardware-available-for-validation)
- [TOYOPUC Computer Link](https://github.com/fa-yoshinobu/plc-comm-computerlink-profiles#verified-hardware-available-for-validation)
- [MC Protocol Serial](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp/blob/main/docsrc/user/PROFILES.md#verified-hardware-available-for-validation)

この環境があるからこそ、新しい機種への対応や、不具合報告の再現・検証を継続的に行い、その結果をライブラリとドキュメントへ反映できます。実機を活かして品質を積み重ねられることが、このプロジェクトの最大の強みだと考えています。

AIも積極的に活用しています。しかし、AIはあくまで開発を支援する道具です。品質を決めるのは、実機による検証、PLCへの理解、仕様の調査、設計の見直し、そして継続的な改善です。

このプロジェクトは、一度完成させて終わるものではありません。PLCの進化とともに成長し続けるライブラリでありたいと考えています。

そして私には、一つの大きな目標があります。

**世界で最も信頼されるPLC通信ライブラリを目指すことです。**

世界一とは、対応機能の数だけを競うことではありません。実機による検証、継続的な改善、正確なドキュメント、利用者からの信頼を積み重ねた結果として、多くの人にそう評価されるライブラリを目指しています。

## English

PLC communication libraries have advanced through the efforts of many people who came before us. I have personally benefited from their work many times.

At the same time, new PLC CPUs, Ethernet units, and communication features continue to appear. Keeping open-source software up to date with them is not easy, and maintaining continuous validation on real hardware is an even greater burden.

I own multiple physical PLCs.

The hardware I own and can use to investigate reported problems is listed by
protocol:

- [MELSEC SLMP](https://github.com/fa-yoshinobu/plc-comm-slmp-profiles#verified-hardware-available-for-validation)
- [KEYENCE KV Host Link](https://github.com/fa-yoshinobu/plc-comm-hostlink-profiles#verified-hardware-available-for-validation)
- [TOYOPUC Computer Link](https://github.com/fa-yoshinobu/plc-comm-computerlink-profiles#verified-hardware-available-for-validation)
- [MC Protocol Serial](https://github.com/fa-yoshinobu/plc-comm-mcprotocol-serial-cpp/blob/main/docsrc/user/PROFILES.md#verified-hardware-available-for-validation)

This environment enables me to continually support new models, reproduce and investigate bug reports, and feed the results back into the libraries and documentation. I believe the ability to build quality over time by putting real hardware to use is this project's greatest strength.

I also make active use of AI. However, AI is only a tool that supports development. Quality is determined by validation on real hardware, an understanding of PLCs, research into specifications, design review, and continuous improvement.

This project is not something to complete once and then leave behind. I want these libraries to continue growing alongside the evolution of PLCs.

And I have one major goal.

**To build the world's most trusted PLC communication libraries.**

Being the best in the world is not about competing solely on the number of supported features. I aim to build libraries that earn that recognition through accumulated real-hardware validation, continuous improvement, accurate documentation, and the trust of their users.
