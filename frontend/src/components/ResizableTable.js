import React, { useState } from 'react';
import { Table } from 'antd';
import { Resizable } from 'react-resizable';
import 'react-resizable/css/styles.css';

const ResizableTable = ({ columns, ...props }) => {
  const [columnWidths, setColumnWidths] = useState({});

  const handleResize = (index) => (e, { size }) => {
    setColumnWidths(prev => ({
      ...prev,
      [index]: size.width
    }));
  };

  const resizableColumns = columns.map((col, index) => ({
    ...col,
    width: columnWidths[index] || col.width,
    onHeaderCell: (column) => ({
      width: columnWidths[index] || column.width,
      onResize: handleResize(index),
    }),
  }));

  const components = {
    header: {
      cell: ResizableCell,
    },
  };

  return (
    <Table
      {...props}
      columns={resizableColumns}
      components={components}
    />
  );
};

const ResizableCell = (props) => {
  const { onResize, width, ...restProps } = props;

  if (!width) {
    return <th {...restProps} />;
  }

  return (
    <Resizable
      width={width}
      height={0}
      handle={
        <span
          className="react-resizable-handle"
          onClick={(e) => {
            e.stopPropagation();
          }}
        />
      }
      onResize={onResize}
      draggableOpts={{ enableUserSelectHack: false }}
    >
      <th {...restProps} />
    </Resizable>
  );
};

export default ResizableTable;
