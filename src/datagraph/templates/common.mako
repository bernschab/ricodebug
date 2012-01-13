<%!
	from datagraphvw import Role
%>\
##
###############################################################################
##
<%def name="open_close_entry(id_, varWrapper)">
%	if varWrapper.isOpen:
		<img style="padding-top:5px" onclick="${id_}.toggleCollapsed()" src="qrc:icons/images/opened.png">
%	else:
		<img style="padding-top:5px" onclick="${id_}.toggleCollapsed()" src="qrc:icons/images/closed.png">
%	endif
</%def>
##
###############################################################################
##
<%def name="simple_entry(role, id_, icon, varWrapper, openclose=False)">
%	if not role == Role.VALUE_ONLY:
	<tr id="${id_}" oncontextmenu="contextmenu(${id_}, '${id_}')";>
		<td nowrap class="varaccess">
<%	if varWrapper.getAccess() in ['private', 'protected']:
		iconprefix = varWrapper.getAccess() + "_"
	else:
		iconprefix = ""
%>\
			<img src="qrc:icons/images/${iconprefix}${icon}">
%		if varWrapper.getAccess():
			<span class="varaccess"> ${varWrapper.getAccess()}</span>
%		endif
		</td>
		<td nowrap class="vartype">
			<span class="vartype"> ${varWrapper.getType()}</span>
		</td>
		<td nowrap class="varname">
			<span class="varname"> ${varWrapper.getExp()}</span>
		</td>
		<td nowrap class="open_close">
%		if openclose:
			${open_close_entry(id_, varWrapper)}
%		else:
			=
%		endif
		</td>
		<td nowrap>
			${caller.body()}
		</td>
	</tr>
%	else:
		${caller.body()}
%	endif
</%def>\
##
###############################################################################
##
<%def name="complex_entry(role, id_, icon, varWrapper)">
%	if role == Role.INCLUDE_HEADER:
	<tr class="header" id="${id}" oncontextmenu="contextmenu(${id}, '${id}')">
		<td nowrap>
			<img src="qrc:icons/images/${icon}">
			<span class="vartype"> ${varWrapper.getType()}</span> 
			<span class="varname"> ${varWrapper.getExp()}</span>
			${open_close_entry(id_, varWrapper)}
		</td>
	</tr>
%		if varWrapper.isOpen:
	<tr id="${id}" oncontextmenu="contextmenu(${id}, '${id}')";>
		<td nowrap>
			<table>
				${caller.body()}
			</table>
		</td>
	</tr>
%		endif
##
%	else:
##
<%call expr="simple_entry(role, id, 'struct.png', varWrapper, True)">
			<table class="variablechild">
%		if varWrapper.isOpen:
			${caller.body()}
%		else:
			<tr id="${id}" oncontextmenu="contextmenu(${id}, '${id}')"><td>...</td></tr>
%		endif
			</table>
</%call>
%	endif
</%def>\