# Examples

示例CIF文件和处理结果。

## 目录结构

- `input/` - 输入的原始CIF文件
  - `1405751.cif` - NH2-UiO-66原始结构（含溶剂）
  - `4512072.cif` - 另一个测试结构
  
- `output/` - 示例输出文件
  - `NH2-UiO-66_desolvated.cif` - 去溶剂后的结构
  - `NH2-UiO-66_2x2x2.cif` - 2x2x2超胞结构

## 使用方法

测试API：
```bash
curl -X POST "http://localhost:8000/api/process" \
  -F "file=@examples/input/1405751.cif" \
  -F "supercell_repeat=[2,2,2]"
```
