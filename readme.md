# ESB接口文档工具  
基于pyqt5实现客户端展示  

## 预计实现功能  
- 接口文档模型库（导入、导出、`编辑`、继承）
- 接口json全节点校验
- 接口文档模板导出（版本隔离、`改动标注`、多文件格式导出） 


## 代办
- 模型细节窗体重构
- 全部子窗口代码整理重构

## 主页窗口
暂未设计


## 模型窗口
特性  
### 模型列表
- 按钮：只存在新增按钮
- 模型列表中有右击菜单
  - 右击模型时：重命名、删除模型
  - 右击空白处：新增模型
- 点击模型，右侧会展示对应的模型展示
- 双击模型：重命名

### 模型展示
#### 按钮部分
- 导入json按钮：输入设计的接口json消息，在合法校验后确定会自动转换成模型，并`保存`展示
- 校验json按钮：按照模型的格式对输入的json进行格式校验
- 保存按钮：在编辑完模型后一定要保存，不然切换模型后就会丢失进度
#### 编辑功能
- 节点的属性可以双击进行编辑（类型是下拉框、必填是单选框）
- 根节点不支持任何编辑
- object、array 类型默认为必填，且不可修改
- array下的items节点名称和类型都不允许编辑

#### 拖拽及菜单功能
- 支持拖拽节点并移到到合适位置（已禁止拖拽array下的items节点）
- 节点只允许放置到object类型里（已禁止放置到array下，只可以放置到items中）
- 右键菜单可以插入节点或对节点进行操作
  - 根节点不支持任何操作
  - object 支持插入子节点，删除节点，在前面（后面）插入节点（注：array下的items只支持插入子节点）
  - array 支持删除节点，在前面（后面）插入节点
  - 在array没有子节点时会多一个增加items选项
  - 普通类型 支持删除节点，在前面（后面）插入节点




## 接口层窗口
暂未设计