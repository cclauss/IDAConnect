import logging

import idc
import ida_idp

# Import ABC and events
from hooks_abc import Hooks
from ..events.events_idb import *


logger = logging.getLogger('IDAConnect.Core')

# -----------------------------------------------------------------------------
# IDB Hooks
# -----------------------------------------------------------------------------


class IDBHooks(ida_idp.IDB_Hooks, Hooks):

    def __init__(self, plugin):
        ida_idp.IDB_Hooks.__init__(self)
        Hooks.__init__(self, plugin)

    def make_code(self, insn):
        self._sendEvent(MakeCodeEvent(insn.ea))
        return 0

    def make_data(self, ea, flags, tid, size):
        self._sendEvent(MakeDataEvent(ea, flags, size, tid))
        return 0

    def renamed(self, ea, new_name, local_name):
        self._sendEvent(RenamedEvent(ea, new_name, local_name))
        return 0

    def func_added(self, func):
        self._sendEvent(FuncAddedEvent(func.startEA, func.endEA))
        return 0

    def deleting_func(self, func):
        self._sendEvent(DeletingFuncEvent(func.startEA))
        return 0

    def set_func_start(self, func, new_start):
        self._sendEvent(SetFuncStartEvent(func.startEA, new_start))
        return 0

    def set_func_end(self, func, new_end):
        self._sendEvent(SetFuncEndEvent(func.startEA, new_end))
        return 0

    def cmt_changed(self, ea, repeatable_cmt):
        cmt = idc.get_cmt(ea, repeatable_cmt)
        cmt = '' if not cmt else cmt
        self._sendEvent(CmtChangedEvent(ea, cmt, repeatable_cmt))
        return 0

    def ti_changed(self, ea, type_, fname):
        py_type = idc.GetTinfo(ea)
        self._sendEvent(TiChangedEvent(ea, py_type))
        return 0

    def op_type_changed(self, ea, n):
        flags = idc.get_full_flags(ea)
        if n == 0:
            if idc.isHex0(flags):
                op = 'hex'
            elif idc.isBin0(flags):
                op = 'bin'
            elif idc.isDec0(flags):
                op = 'dec'
            elif idc.isChar0(flags):
                op = 'chr'
            elif idc.isOct0(flags):
                op = 'oct'
            else:
                raise NotImplementedError("type not supported")
        else:
            if idc.isHex1(flags):
                op = 'hex'
            elif idc.isBin1(flags):
                op = 'bin'
            elif idc.isDec1(flags):
                op = 'dec'
            elif idc.isChar1(flags):
                op = 'chr'
            elif idc.isOct1(flags):
                op = 'oct'
            else:
                raise NotImplementedError("type not supported")
        self._sendEvent(OpTypeChangedEvent(ea, n, op))
        return 0