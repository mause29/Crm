import React, { useState } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const initialTasks = [
    { id: '1', content: 'Llamar a cliente A' },
    { id: '2', content: 'Enviar cotización' },
    { id: '3', content: 'Revisión de contrato' }
];

export default function Dashboard({ socket }) {
    const [tasks, setTasks] = useState(initialTasks);

    const onDragEnd = result => {
        if (!result.destination) return;
        const items = Array.from(tasks);
        const [reordered] = items.splice(result.source.index, 1);
        items.splice(result.destination.index, 0, reordered);
        setTasks(items);
    };

    const sendNotification = () => socket.emit('notify', 'Se actualizó una tarea');

    return (
        <div className="p-4">
            <button onClick={sendNotification} className="mb-4 px-4 py-2 bg-green-500 text-white rounded">Enviar Notificación</button>
            <DragDropContext onDragEnd={onDragEnd}>
                <Droppable droppableId="tasks">
                    {provided => (
                        <div {...provided.droppableProps} ref={provided.innerRef}>
                            {tasks.map((task, index) => (
                                <Draggable key={task.id} draggableId={task.id} index={index}>
                                    {provided => (
                                        <div
                                            ref={provided.innerRef}
                                            {...provided.draggableProps}
                                            {...provided.dragHandleProps}
                                            className="p-4 mb-2 bg-gray-200 rounded cursor-pointer hover:bg-gray-300 transition"
                                        >
                                            {task.content}
                                        </div>
                                    )}
                                </Draggable>
                            ))}
                            {provided.placeholder}
                        </div>
                    )}
                </Droppable>
            </DragDropContext>
        </div>
    );
}
