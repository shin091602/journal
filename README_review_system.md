# LaTeX Paper Review System

論文のファイルの誤字脱字や形式の確認を行うための包括的なレビューシステムです。

## 機能

### 1. 誤字脱字チェック (`spell_checker.py`)
- 一般的な誤字脱字の検出
- 重複した単語の検出
- 学術論文でよく使われる技術用語の認識

### 2. LaTeX構文検証 (`latex_validator.py`)
- 括弧の対応チェック
- begin/end環境の対応チェック
- 図表の参照確認
- 数式環境の検証
- 一般的なLaTeX構文エラーの検出

### 3. 学術文体チェック (`academic_style_checker.py`)
- 学術論文に不適切な表現の検出
- 冗長な表現の指摘
- 曖昧な表現の改善提案
- 人称代名詞の使用チェック
- 文章構造の分析

### 4. 統合レビューシステム (`paper_reviewer.py`)
- 上記すべての機能を統合
- 包括的なレポート生成
- 優先度付きの改善提案

## 使用方法

### 個別ツールの使用

```bash
# 誤字脱字チェック
python spell_checker.py ISTS_shin.tex

# LaTeX構文検証
python latex_validator.py ISTS_shin.tex

# 学術文体チェック
python academic_style_checker.py ISTS_shin.tex
```

### 統合レビューシステム（推奨）

```bash
# 包括的なレビュー実行
python paper_reviewer.py ISTS_shin.tex
```

このコマンドは以下を実行します：
1. すべてのチェックを実行
2. 包括的なレポートを表示
3. レポートファイル（`ISTS_shin_review_report.txt`）を生成

## 出力例

```
📋 PAPER REVIEW REPORT
File: ISTS_shin.tex
================================================================================

📊 SUMMARY
----------------------------------------
Total issues found: 15
• Spelling/Typos: 3
• LaTeX Syntax: 5
• Style Suggestions: 7

📝 SPELLING AND TYPOS
----------------------------------------
Line 72: 'seciton' should be 'section'
  → detection using a Poincaré seciton.

🔧 LATEX SYNTAX ISSUES
----------------------------------------
Line 23: Duplicated package - graphicx loaded twice
  → \usepackage{graphicx}

✍️  ACADEMIC STYLE SUGGESTIONS
----------------------------------------
Line 111: Wordy expression 'in recent years' → Consider: recently
  → In recent years, the resurgence of space exploration...
```

## ファイル構成

- `spell_checker.py` - 誤字脱字チェッカー
- `latex_validator.py` - LaTeX構文検証器
- `academic_style_checker.py` - 学術文体チェッカー
- `paper_reviewer.py` - 統合レビューシステム
- `test_review_system.py` - システムテスト用スクリプト
- `README_review_system.md` - このファイル

## 要件

- Python 3.6以上
- 標準ライブラリのみ使用（追加インストール不要）

## 特徴

### 誤字脱字チェック
- 英語/日本語混在対応
- 学術用語の適切な認識
- 文脈を考慮した提案

### LaTeX構文検証
- 包括的な構文エラー検出
- 図表参照の整合性確認
- 数式環境の検証

### 学術文体チェック
- 学術論文に適した表現の提案
- 冗長性の削減
- 明確性の向上

## 注意事項

1. このツールは補助的なものです。最終的な判断は著者が行ってください。
2. 技術用語や専門用語については、分野固有の辞書と照合することをお勧めします。
3. LaTeX構文エラーについては、実際にコンパイルして確認することをお勧めします。

## カスタマイズ

各チェッカーのルールは対応するPythonファイル内で調整できます：
- `spell_checker.py`: `common_misspellings`辞書
- `academic_style_checker.py`: `informal_expressions`、`wordy_expressions`辞書
- `latex_validator.py`: 検証ルールの追加・変更

## トラブルシューティング

問題が発生した場合：
1. Python 3.6以上がインストールされていることを確認
2. すべてのファイルが同じディレクトリにあることを確認
3. `python test_review_system.py`でシステムテストを実行