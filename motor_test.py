# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt
import numpy as np
import wx
import os.path
import motor


# 上位机测试程序主窗口
class main_frame(wx.Frame):

    def __init__(self, parent, title):
        self.filename = title
        self.dirname = '.'
        wx.Frame.__init__(self, parent, title=title)
        self.motor_data = {}
        self.data_list = {}
        self.print_txt = ""
        self.motor_data_num = 0
        self.create_menu()
        self.create_frame_panel()
        self.do_layout()
        self.button_bind()

    # 显示面板
    def create_frame_panel(self):
        self.data_list_label = wx.StaticText(
            self, label=u"导入数据列表:")
        self.data_list = wx.ListView(self, size=(400, 300))
        self.data_list.InsertColumn(0, u'文件名', width=200)
        self.data_list.InsertColumn(1, u'长度', width=200)
        self.button_input = wx.Button(self, label=u"导入数据(&I)")
        self.button_delete = wx.Button(self, label=u"删除数据(&D)")
        self.button_join = wx.Button(self, label=u"合并数据(&J)")
        self.button_display = wx.Button(self, label=u"显示数据(&P)")
        self.button_statistics = wx.Button(self, label=u"统计特性(&S)")
        self.button_plot = wx.Button(self, label=u"绘制图像(&L)")
        self.button_calculate = wx.Button(self, label=u"参数估计(&C)")
        self.button_print = wx.Button(self, label=u"打印报告(&R)")

    # 设置格式
    def do_layout(self):
        self.box_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.grid_sizer = wx.FlexGridSizer(rows=6, cols=2, vgap=10, hgap=10)
        self.list_sizer = wx.BoxSizer(orient=wx.VERTICAL)

        # self.list_sizer.Clear()

        expand_option = dict(flag=wx.EXPAND)
        no_options = dict()
        empty_space = ((0, 0), no_options)

        for control, options in \
            [(self.button_input, no_options),
             (self.button_statistics, no_options),
             (self.button_delete, no_options),
             (self.button_plot, no_options),
             (self.button_join, no_options),
             (self.button_calculate, no_options),
             (self.button_display, no_options),
             (self.button_print, no_options)]:
            self.grid_sizer.Add(control, **options)

        for control, options in \
            [(self.data_list_label, expand_option),
             (self.data_list, expand_option)]:
            self.list_sizer.Add(control, **options)

        for control, options in \
            [(self.list_sizer, dict(border=5, flag=wx.ALL | wx.EXPAND)),
             (self.grid_sizer, dict(border=5, flag=wx.ALL | wx.EXPAND))]:
            self.box_sizer.Add(control, **options)

        self.SetSizerAndFit(self.box_sizer)

    # 帮助信息
    def default_file_dialog_options(self):
        ''' Return a dictionary with file dialog options that can be
                used in both the save file dialog as well as in the open
                file dialog. '''
        return dict(message='Choose a file', defaultDir=self.dirname,
                    wildcard='*.*')

    # 得到文件名
    def ask_user_for_filename(self, **dialogOptions):
        dialog = wx.FileDialog(self, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            user_provided_filename = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()

        else:
            user_provided_filename = False
        dialog.Destroy()
        return user_provided_filename

    # 创建按钮单击事件
    def button_bind(self):
        self.Bind(wx.EVT_BUTTON, self.data_input, self.button_input)
        self.Bind(wx.EVT_BUTTON, self.data_delete, self.button_delete)
        self.Bind(wx.EVT_BUTTON, self.data_join, self.button_join)
        self.Bind(wx.EVT_BUTTON, self.data_display, self.button_display)
        self.Bind(wx.EVT_BUTTON, self.data_plot, self.button_plot)
        self.Bind(wx.EVT_BUTTON, self.data_calculate, self.button_calculate)
        self.Bind(wx.EVT_BUTTON, self.data_statistics, self.button_statistics)
        self.Bind(wx.EVT_BUTTON, self.on_save_as, self.button_print)

    # 导入数据
    def data_input(self, event):
        if self.ask_user_for_filename(style=wx.OPEN,
                                      **self.default_file_dialog_options()):
            textfile = open(os.path.join(self.dirname, self.filename), 'r')

            # self.motor_data.append(motor.data(
            #     os.path.join(self.dirname, self.filename)))
            motor_init = motor.data(
                os.path.join(self.dirname, self.filename))
            self.motor_data[self.filename] = motor_init
            num_items = self.data_list.GetItemCount()
            self.data_list.InsertStringItem(num_items, self.filename)
            self.data_list.SetStringItem(
                num_items, 1, unicode(motor_init.get_num()))
            self.motor_data_num = self.motor_data_num + 1
            textfile.close()

    # 删除数据
    def data_delete(self, event):
        while(self.data_list.GetFirstSelected() is not -1):
            self.data_list.DeleteItem(self.data_list.GetFirstSelected())

        # delete_data = []
        # delete_data.append(self.data_list.GetFirstSelected())
        # print self.data_list.GetSelectedItemCount()
        # for i in range(1, self.data_list.GetSelectedItemCount()):
        #     print self.data_list.GetNextSelected(delete_data[-1])
        #     delete_data.append(self.data_list.GetNextSelected(delete_data[-1]))

        # for i in range(0, self.data_list.GetSelectedItemCount()):
        #     print delete_data[i]
        #     self.data_list.DeleteItem(delete_data[i])
        # delete_item = self.data_list.GetFocusedItem()
        # self.data_list.DeleteItem(delete_item)

    # 合并数据
    def data_join(self, event):
        join_data = []
        selected_num = self.data_list.GetSelectedItemCount()
        join_data.append(self.data_list.GetFirstSelected())
        for i in range(1, selected_num):
            join_data.append(self.data_list.GetNextSelected(join_data[-1]))

        # motor_data = self.motor_data[join_data[0].getI]
        for i in range(0, selected_num):
            join_data[i] = self.data_list.GetItemText(join_data[i])
            print join_data[i]

        motor_data = self.motor_data[join_data[0]]
        item_txt = '%s ' % join_data[0]
        for i in range(1, selected_num):
            motor_data_join = self.motor_data[join_data[i]].get_init_data()
            motor_data.data_join(motor_data_join)
            item_txt = item_txt + '%s ' % join_data[i]

        num_items = self.data_list.GetItemCount()

        self.motor_data[item_txt] = motor_data
        self.data_list.InsertStringItem(num_items, item_txt)
        self.data_list.SetStringItem(
            num_items, 1, unicode(motor_data.get_num()))

    # 显示数据
    def data_display(self, event):
        calculate_data = []
        selected_num = self.data_list.GetSelectedItemCount()
        calculate_data.append(self.data_list.GetFirstSelected())
        for i in range(1, selected_num):
            calculate_data.append(
                self.data_list.GetNextSelected(calculate_data[-1]))

        for i in range(0, selected_num):
            calculate_data[i] = self.data_list.GetItemText(calculate_data[i])
            display_window = display_frame(
                self, calculate_data[i], self.motor_data[calculate_data[i]])
            display_window.Show()

    # 绘图
    def data_plot(self, event):
        calculate_data = []
        selected_num = self.data_list.GetSelectedItemCount()
        calculate_data.append(self.data_list.GetFirstSelected())
        for i in range(1, selected_num):
            calculate_data.append(
                self.data_list.GetNextSelected(calculate_data[-1]))

        for i in range(0, selected_num):
            calculate_data[i] = self.data_list.GetItemText(calculate_data[i])
            data = self.motor_data[calculate_data[i]].get_data()
            plt.figure(i)
            plt.subplot(3, 1, 1)
            plt.title('U-t')
            plt.xlabel('t/s')
            plt.ylabel('U/V')
            plt.plot(data[:, 0], data[:, 1])
            plt.subplot(3, 1, 2)
            plt.title('I-t')
            plt.xlabel('t/s')
            plt.ylabel('I/A')
            plt.plot(data[:, 0], data[:, 2])
            plt.subplot(3, 1, 3)
            plt.title('w-t')
            plt.xlabel('t/s')
            plt.ylabel('w/rad/s')
            plt.plot(data[:, 0], data[:, 3])
        plt.show()

    def data_calculate(self, event):
        calculate_data = []
        selected_num = self.data_list.GetSelectedItemCount()
        calculate_data.append(self.data_list.GetFirstSelected())
        for i in range(1, selected_num):
            calculate_data.append(
                self.data_list.GetNextSelected(calculate_data[-1]))

        for i in range(0, selected_num):
            calculate_data[i] = self.data_list.GetItemText(calculate_data[i])
            calculate_window = calculate_frame(
                self, calculate_data[i], self.motor_data[calculate_data[i]])
            calculate_window.Show()

    def data_statistics(self, event):
        statistics_data = []
        selected_num = self.data_list.GetSelectedItemCount()
        statistics_data.append(self.data_list.GetFirstSelected())
        for i in range(1, selected_num):
            statistics_data.append(
                self.data_list.GetNextSelected(statistics_data[-1]))

        for i in range(0, selected_num):
            statistics_data[i] = self.data_list.GetItemText(statistics_data[i])
            statistics_window = statistics_frame(
                self, statistics_data[i], self.motor_data[statistics_data[i]])
            statistics_window.Show()

    # 创建菜单栏
    def create_menu(self):
        file_menu = wx.Menu()
        for id, label, help_text, handler in \
                [(wx.ID_ABOUT, u'关于(&A)', u'程序相关信息',
                  self.on_about),
                 (wx.ID_HELP, u'帮助(&H)', u'打开帮助文档', self.on_help),
                 (wx.ID_EXIT, u'退出(&E)', u'退出程序', self.on_exit)]:
            if id == None:
                file_menu.AppendSeparator()
            else:
                item = file_menu.Append(id, label, help_text)
                self.Bind(wx.EVT_MENU, handler, item)
        menu_bar = wx.MenuBar()
        # Add the fileMenu to the MenuBar
        menu_bar.Append(file_menu, u'文件(&F)')
        self.SetMenuBar(menu_bar)  # Add the menuBar to the Frame
        self.CreateStatusBar()

    # 设置标题
    def set_title(self, children_window):
        super(children, self).SetTitle('Editor %s' %
                                       self.filename)  # 重写wx的SetTitle方法

    # 事件处理
    def on_about(self, event):
        dialog = wx.MessageDialog(self, u'同济大学TUSmart智能车队\n'
                                  u'电机测试台项目小组', '关于', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def on_exit(self, event):
        self.Close()  # Close the main window.

    # def on_save(self, event):
    #     textfile = open(os.path.join(self.dirname, self.filename), 'w')
    #     textfile.write(self.control.GetValue())
    #     textfile.close()

    # def on_open(self, event):
    #     if self.ask_user_for_filename(style=wx.OPEN,
    #                                   **self.default_file_dialog_options()):
    #         textfile = open(os.path.join(self.dirname, self.filename), 'r')
    #         # self.motor_init = motor.data(
    #         #     os.path.join(self.dirname, self.filename))
    #         motor_init = motor.data(
    #             os.path.join(self.dirname, self.filename))
    #         self.data_list[self.filename] = motor_init

    #         textfile.close()

    def on_help(self, event):
        help_window = help_txt(self, u"电机测试台上位机使用帮助文档")
        help_window.Show()

    def on_save_as(self, event):
        print_data = []
        selected_num = self.data_list.GetSelectedItemCount()
        print_data.append(self.data_list.GetFirstSelected())
        for i in range(1, selected_num):
            print_data.append(
                self.data_list.GetNextSelected(print_data[-1]))

        for i in range(0, selected_num):
            print_data[i] = self.data_list.GetItemText(print_data[i])
            data_print = self.motor_data[print_data[i]]
            self.print_txt = "#电机试验台计算结果报告\n"
            self.print_txt = self.print_txt + "\n##原始数据的统计结果为：\n"
            self.print_txt = self.print_txt + \
                "\n|　  |电压(V)|电流(A)|角速度(rad/s)|\n"
            self.print_txt = self.print_txt + "|----|-------|-------|-------------|\n"
            self.print_txt = self.print_txt + "|平均值|%s|%s|%s|\n" % (data_print.get_data_mean(
            )['voltage'], data_print.get_data_mean()['current'], data_print.get_data_mean()['roll_rate'])
            self.print_txt = self.print_txt + "|方差|%s|%s|%s|\n" % (data_print.get_data_var(
            )['voltage'], data_print.get_data_var()['current'], data_print.get_data_var()['roll_rate'])

            self.print_txt = self.print_txt + "\n##参数计算结果为：\n"
            self.print_txt = self.print_txt + "\n###不考虑摩擦转矩的计算结果为：\n"
            self.print_txt = self.print_txt + "|　  |k_E|L_m|R_m|\n"
            self.print_txt = self.print_txt + "|----|-------|-------|-------------|\n"
            self.print_txt = self.print_txt + "| |%s|%s|%s|\n" % (data_print.get_solve('easy'
                                                                                       )['k_E'], data_print.get_solve('easy')['L_m'], data_print.get_solve('easy')['R_m'])
            self.print_txt = self.print_txt + "|平均值|%s|%s|%s|\n" % (data_print.get_check_mean('easy'
                                                                                              )['k_E'], data_print.get_check_mean('easy')['L_m'], data_print.get_check_mean('easy')['R_m'])
            self.print_txt = self.print_txt + "|方差|%s|%s|%s|\n" % (data_print.get_check_var('easy'
                                                                                            )['k_E'], data_print.get_check_var('easy')['L_m'], data_print.get_check_var('easy')['R_m'])
            self.print_txt = self.print_txt + "\n###考虑摩擦转矩的计算结果为：\n"
            self.print_txt = self.print_txt + "|　  |k_E|L_m|R_m|f_m|\n"
            self.print_txt = self.print_txt + "|----|-------|-------|-------|------|\n"
            self.print_txt = self.print_txt + "| |%s|%s|%s|%s|\n" % (data_print.get_solve('hard'
                                                                                          )['k_E'], data_print.get_solve('hard')['L_m'], data_print.get_solve('hard')['R_m'], data_print.get_solve('hard')['f_m'])
            self.print_txt = self.print_txt + "|平均值|%s|%s|%s|%s|\n" % (data_print.get_check_mean('hard'
                                                                                                 )['k_E'], data_print.get_check_mean('hard')['L_m'], data_print.get_check_mean('hard')['R_m'], data_print.get_check_mean('hard')['f_m'])
            self.print_txt = self.print_txt + "|方差|%s|%s|%s|%s|\n" % (data_print.get_check_var('hard'
                                                                                               )['k_E'], data_print.get_check_var('hard')['L_m'], data_print.get_check_var('hard')['R_m'], data_print.get_check_var('hard')['f_m'])
            self.print_txt = self.print_txt + \
                "\n注意：以上平均值与方差都是将数据平均分为%s组后分别计算的统计结果\n" % data_print.get_group_num()
            if self.ask_user_for_filename(defaultFile=self.filename, style=wx.SAVE,
                                          **self.default_file_dialog_options()):
                self.on_save(event)

    def on_save(self, event):
        textfile = open(os.path.join(self.dirname, self.filename), 'w')
        textfile.write(self.print_txt)
        textfile.close()


class display_frame(wx.Frame):
    def __init__(self, parent, title, data):
        self.dirname = ''
        wx.Frame.__init__(self, parent, title=title, size=(800, 800))
        self.data_list = wx.ListView(self, size=(800, 800))
        self.data_list.InsertColumn(0, u'时间(s)', width=200)
        self.data_list.InsertColumn(1, u'电压(V)', width=200)
        self.data_list.InsertColumn(2, u'电流(A)', width=200)
        self.data_list.InsertColumn(3, u'角速度(rad/s)', width=200)

        for i in range(0, data.get_num()):
            num_items = self.data_list.GetItemCount()
            self.data_list.InsertStringItem(
                num_items, unicode(data.get_data()[i, 0]))
            self.data_list.SetStringItem(
                num_items, 1, unicode(data.get_data()[i, 1]))
            self.data_list.SetStringItem(
                num_items, 2, unicode(data.get_data()[i, 2]))
            self.data_list.SetStringItem(
                num_items, 3, unicode(data.get_data()[i, 3]))


class statistics_frame(wx.Frame):
    def __init__(self, parent, title, data):
        self.dirname = ''
        wx.Frame.__init__(self, parent, title=title, size=(800, 300))
        self.data_list = wx.ListView(self, size=(800, 800))
        self.data_list.InsertColumn(0, u' ', width=200)
        self.data_list.InsertColumn(1, u'电压(V)', width=200)
        self.data_list.InsertColumn(2, u'电流(A)', width=200)
        self.data_list.InsertColumn(3, u'角速度(rad/s)', width=200)

        self.data_list.InsertStringItem(
            0, u'平均值')
        self.data_list.SetStringItem(
            0, 1, unicode(data.get_data_mean()['voltage']))
        self.data_list.SetStringItem(
            0, 2, unicode(data.get_data_mean()['current']))
        self.data_list.SetStringItem(
            0, 3, unicode(data.get_data_mean()['roll_rate']))

        self.data_list.InsertStringItem(
            1, u'方差')
        self.data_list.SetStringItem(
            1, 1, unicode(data.get_data_var()['voltage']))
        self.data_list.SetStringItem(
            1, 2, unicode(data.get_data_var()['current']))
        self.data_list.SetStringItem(
            1, 3, unicode(data.get_data_var()['roll_rate']))


class calculate_frame(wx.Frame):
    def __init__(self, parent, title, data):
        self.dirname = ''
        wx.Frame.__init__(self, parent, title=title, size=(600, 500))
        self.data_list_label1 = wx.StaticText(self, label=u"不考虑摩擦转矩的计算结果为：")
        self.data_list_label2 = wx.StaticText(self, label=u"考虑摩擦转矩的计算结果为：")
        self.data_list1 = wx.ListView(self, size=(600, 100))
        self.data_list1.InsertColumn(0, 'k_E', width=150)
        self.data_list1.InsertColumn(1, 'L_m', width=150)
        self.data_list1.InsertColumn(2, 'R_m', width=150)

        self.data = data

        self.data_note = wx.StaticText(
            self, label=u"为计算统计特性，需要对数据分组计算，请输入分组个数：")
        self.data_text = wx.TextCtrl(self)
        self.data_button = wx.Button(self, label=u"输出结果")

        self.data_list1.InsertStringItem(
            0, unicode(data.get_solve('easy')['k_E']))
        self.data_list1.SetStringItem(
            0, 1, unicode(data.get_solve('easy')['L_m']))
        self.data_list1.SetStringItem(
            0, 2, unicode(data.get_solve('easy')['R_m']))

        self.data_list2 = wx.ListView(self, size=(600, 100))
        self.data_list2.InsertColumn(0, 'k_E', width=150)
        self.data_list2.InsertColumn(1, 'L_m', width=150)
        self.data_list2.InsertColumn(2, 'R_m', width=150)
        self.data_list2.InsertColumn(3, 'f_m', width=150)

        self.data_list2.InsertStringItem(
            0, unicode(data.get_solve('hard')['k_E']))
        self.data_list2.SetStringItem(
            0, 1, unicode(data.get_solve('hard')['L_m']))
        self.data_list2.SetStringItem(
            0, 2, unicode(data.get_solve('hard')['R_m']))
        self.data_list2.SetStringItem(
            0, 3, unicode(data.get_solve('hard')['f_m']))

        self.text_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        expand_option = dict(flag=wx.EXPAND)
        no_options = dict()
        empty_space = ((0, 0), no_options)
        for control, options in \
            [(self.data_note, no_options),
             (self.data_text, no_options)]:
            self.text_sizer.Add(control, **options)
        for control, options in \
            [(self.data_list_label1, no_options),
             (self.data_list1, no_options),
             (self.data_list_label2, no_options),
             (self.data_list2, no_options),
             (self.text_sizer, no_options),
             (self.data_button, dict(flag=wx.ALIGN_CENTER))]:
            self.box_sizer.Add(control, **options)

        self.SetSizerAndFit(self.box_sizer)
        self.Bind(wx.EVT_BUTTON, self.data_print, self.data_button)

    def data_print(self, event):
        group_num = int(self.data_text.GetValue())
        frame = data_print_frame(self, u'估计结果统计特性分析', self.data, group_num)
        frame.Show()


class data_print_frame(wx.Frame):
    def __init__(self, parent, title, data, group_num):
        self.dirname = ''
        wx.Frame.__init__(self, parent, title=title, size=(600, 500))
        self.data_list_label1 = wx.StaticText(self, label=u"不考虑摩擦转矩的计算结果为：")
        self.data_list_label2 = wx.StaticText(self, label=u"考虑摩擦转矩的计算结果为：")
        self.data_list1 = wx.ListView(self, size=(750, 400))
        self.data_list1.InsertColumn(0, u'组数', width=150)
        self.data_list1.InsertColumn(1, 'k_E', width=150)
        self.data_list1.InsertColumn(2, 'L_m', width=150)
        self.data_list1.InsertColumn(3, 'R_m', width=150)

        self.data_list2 = wx.ListView(self, size=(750, 400))
        self.data_list2.InsertColumn(0, u'组数', width=150)
        self.data_list2.InsertColumn(1, 'k_E', width=150)
        self.data_list2.InsertColumn(2, 'L_m', width=150)
        self.data_list2.InsertColumn(3, 'R_m', width=150)
        self.data_list2.InsertColumn(4, 'f_m', width=150)

        for i in range(0, group_num):
            self.data_list1.InsertStringItem(i, unicode(i + 1))
            self.data_list1.SetStringItem(
                i, 1, unicode(data.get_check('easy')['k_E'][i, 0]))
            self.data_list1.SetStringItem(
                i, 2, unicode(data.get_check('easy')['L_m'][i, 0]))
            self.data_list1.SetStringItem(
                i, 3, unicode(data.get_check('easy')['R_m'][i, 0]))
        self.data_list1.InsertStringItem(group_num, u'平均值')
        self.data_list1.SetStringItem(
            group_num, 1, unicode(data.get_check_mean('easy')['k_E']))
        self.data_list1.SetStringItem(
            group_num, 2, unicode(data.get_check_mean('easy')['L_m']))
        self.data_list1.SetStringItem(
            group_num, 3, unicode(data.get_check_mean('easy')['R_m']))
        self.data_list1.InsertStringItem(group_num + 1, u'方差')
        self.data_list1.SetStringItem(
            group_num + 1, 1, unicode(data.get_check_var('easy')['k_E']))
        self.data_list1.SetStringItem(
            group_num + 1, 2, unicode(data.get_check_var('easy')['L_m']))
        self.data_list1.SetStringItem(
            group_num + 1, 3, unicode(data.get_check_var('easy')['R_m']))

        for i in range(0, group_num):
            self.data_list2.InsertStringItem(i, unicode(i + 1))
            self.data_list2.SetStringItem(
                i, 1, unicode(data.get_check('hard')['k_E'][i, 0]))
            self.data_list2.SetStringItem(
                i, 2, unicode(data.get_check('hard')['L_m'][i, 0]))
            self.data_list2.SetStringItem(
                i, 3, unicode(data.get_check('hard')['R_m'][i, 0]))
            self.data_list2.SetStringItem(
                i, 4, unicode(data.get_check('hard')['f_m'][i, 0]))
        self.data_list2.InsertStringItem(group_num, u'平均值')
        self.data_list2.SetStringItem(
            group_num, 1, unicode(data.get_check_mean('hard')['k_E']))
        self.data_list2.SetStringItem(
            group_num, 2, unicode(data.get_check_mean('hard')['L_m']))
        self.data_list2.SetStringItem(
            group_num, 3, unicode(data.get_check_mean('hard')['R_m']))
        self.data_list2.SetStringItem(
            group_num, 4, unicode(data.get_check_mean('hard')['f_m']))
        self.data_list2.InsertStringItem(group_num + 1, u'方差')
        self.data_list2.SetStringItem(
            group_num + 1, 1, unicode(data.get_check_var('hard')['k_E']))
        self.data_list2.SetStringItem(
            group_num + 1, 2, unicode(data.get_check_var('hard')['L_m']))
        self.data_list2.SetStringItem(
            group_num + 1, 3, unicode(data.get_check_var('hard')['R_m']))
        self.data_list2.SetStringItem(
            group_num + 1, 4, unicode(data.get_check_var('hard')['f_m']))

        expand_option = dict(flag=wx.EXPAND)
        no_options = dict()
        empty_space = ((0, 0), no_options)
        self.box_sizer = wx.BoxSizer(orient=wx.VERTICAL)
        for control, options in \
            [(self.data_list_label1, no_options),
             (self.data_list1, no_options),
             (self.data_list_label2, no_options),
             (self.data_list2, no_options)]:
            self.box_sizer.Add(control, **options)

        self.SetSizerAndFit(self.box_sizer)


class help_txt(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''
        wx.Frame.__init__(self, parent, title=title, size=(600, 500))
        self.help_text = u"\n导入数据：点击按钮，可以选择需要的文档，将数据导入界面\n"
        self.help_text = self.help_text + u"\n删除数据：选中需删除的项目，点击此按钮，数据不再在界面中\n"
        self.help_text = self.help_text + u"\n合并数据：可选择多个数据，点此按钮后，合并为一个新的数据\n"
        self.help_text = self.help_text + u"\n显示数据：将选中的项目显示出来\n"
        self.help_text = self.help_text + u"\n统计特性：显示选中项目的均值及方差\n"
        self.help_text = self.help_text + u"\n绘制图像：用项目中的数据绘制出图像\n"
        self.help_text = self.help_text + \
            u"\n参数估计：得到不考虑摩擦转矩时的k_E、L_m、R_m，以及考虑摩擦转矩时的k_E、L_m、R_m、f_m\n"
        self.help_text = self.help_text + u"\n打印报告：生成一份包含实验参数的文档报告\n"
        self.txt = wx.TextCtrl(self, value=self.help_text,
                               style=wx.TE_MULTILINE | wx.TE_READONLY)


app = wx.App(False)
frame = main_frame(None, u"电机测试台上位机程序")
frame.Show()
app.MainLoop()
