'''

Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

The SIF header format is developed and licensed by Sylabs,
see https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go

'''

class Deffile:
    '''A SIF Deffile descriptor is read after the global header See
       https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go for details
       This isn't a class with functions, just an organizational structure
       for fields and the format string.    

       # Datatype  int32   <1i
       # Used      bool    ?
       # ID        uint32  I 
       # Groupid   uint32  I 
       # Link      uint32  I 
       # Fileoff   int64   q
       # Filelen   int64   q
       # Storelen  int64   q
       # Ctime     int64   q       
       # Mtime     int64   q              
       # UID       int64   q              
       # Gid       int64   q              

       # TODO these two aren't parsed yet
       # Name  [DescrNameLen]byte    self.base.DescrNameLen
       # Extra [DescrMaxPrivLen]byte // big enough for extra data below

    '''

    fields = [
                   "Datatype",  
                   "Used",
                   "ID",
                   "Groupid",
                   "Link",
                   "Fileoff",
                   "Filelen",
                   "Storelen",
                   "Ctime",
                   "Mtime",
                   "UID",
                   "Gid"     ]

    # Format string to read in above
    fmt = '<i?3I7q'

    def __str__(self):
        return "SIF Descriptor Definition Version 02"

    def __repr__(self):
        return self.__str__()

