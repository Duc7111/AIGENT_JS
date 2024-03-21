import React from 'react';

const Directorylist = () => {
    // Sample directory data
    const directories = [
        { name: 'Directory 1', icons: ['icon1', 'icon2', 'icon3', 'icon4'] },
        { name: 'Directory 2', icons: ['icon1', 'icon2', 'icon3', 'icon4'] },
        { name: 'Directory 3', icons: ['icon1', 'icon2', 'icon3', 'icon4'] },
        // Add more directories as needed
    ];

    return (
        <div>
            {directories.map((directory, index) => (
                <div key={index} onClick={() => handleDirectoryClick(directory)}>
                    <h3>{directory.name}</h3>
                    <div>
                        {directory.icons.map((icon, iconIndex) => (
                            <img key={iconIndex} src={icon} alt={`Icon ${iconIndex + 1}`} />
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Directorylist;