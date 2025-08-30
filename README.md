# 🕷️ NotemsSpider

> Collects note content from [note.ms](https://note.ms)

[![GitHub License](https://img.shields.io/github/license/Sn0wo2/NotemsSpider)](LICENSE)
[![Python CI](https://github.com/Sn0wo2/NotemsSpider/actions/workflows/python.yml/badge.svg)](https://github.com/Sn0wo2/NotemsSpider/actions/workflows/python.yml)
[![CodeQL Advanced](https://github.com/Sn0wo2/NotemsSpider/actions/workflows/codeql.yml/badge.svg)](https://github.com/Sn0wo2/NotemsSpider/actions/workflows/codeql.yml)
[![Dependabot Updates](https://github.com/Sn0wo2/NotemsSpider/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/Sn0wo2/NotemsSpider/actions/workflows/dependabot/dependabot-updates)
[![Automatic Dependency Submission](https://github.com/Sn0wo2/NotemsSpider/actions/workflows/dependency-graph/auto-submission/badge.svg)](https://github.com/Sn0wo2/NotemsSpider/actions/workflows/dependency-graph/auto-submission)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FSn0wo2%2FNotemsSpider.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FSn0wo2%2FNotemsSpider?ref=badge_shield)

---

## ✏️ About Writing Notes

We **do not** support or encourage automated bulk writing to [note.ms](https://note.ms) in order to preserve the integrity of its valuable(?) content. Therefore, this project will not implement automated note submission.

我们**不**支持或鼓励对 [note.ms](https://note.ms) 进行自动化批量写入，以保护其珍贵(?)内容的完整性。因此本项目不会实现自动写入功能。

## 🚦 Rate Limit Notice

[`config.py`](config.py) should not use high speed. [note.ms](https://note.ms) has an `nginx` **403** rate limit.  
In theory, for the same **IP**, [note.ms](https://note.ms) restricts just enough to prevent concurrency, so there's no need for concurrent crawling.  
**Please do not put excessive load on the [note.ms](https://note.ms) server.**

[`config.py`](config.py)速度不要高, [note.ms](https://note.ms)有`nginx`**403**限速  
按理来说相同**ip**下[note.ms](https://note.ms)的限制是刚好不能并发的, 所以没必要并发爬  
**请不要对[note.ms](https://note.ms)服务器造成过大的压力**

---

## 📜 Disclaimer

```
This script is intended for educational and research purposes only. Use responsibly and ensure compliance with all applicable laws and terms of service.
本脚本仅供教育和研究用途。请负责任地使用，并确保遵守所有适用的法律和服务条款。

If you are the administrator of note.ms and wish this project to be taken down, please open an issue on the repository.
如果您是 note.ms 的网站管理员并希望删除本项目，请在本仓库提交 Issue。
```

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FSn0wo2%2FNotemsSpider.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FSn0wo2%2FNotemsSpider?ref=badge_large)