// client/src/components/Dashboard.js
import React, { useState, useEffect } from 'react';
import { Line, Pie } from 'react-chartjs-2';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

export default function Dashboard({ tasks, sales }) {
  const [taskList, setTaskList] = useState(tasks);

  function handleDragEnd(result) {
    if (!result.destination) return;
    const items = Array.from(taskList);
    const [reordered] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reordered);
    setTaskList(items);
  }

  return (
    <div>
      <h1>Dashboard Interactivo</h1>
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="tasks">
          {provided => (
            <div {...provided.droppableProps} ref={provided.innerRef}>
              {taskList.map((task, index) => (
                <Draggable key={task.id} draggableId={task.id} index={index}>
                  {provided => (
                    <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
                      {task.name}
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
      <Line data={sales} />
      <Pie data={sales} />
    </div>
  );
}
